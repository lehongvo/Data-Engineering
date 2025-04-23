from fastapi import FastAPI, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from web3 import Web3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from web3.exceptions import BlockNotFound
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("app.log")],
)
logger = logging.getLogger(__name__)


# Database configuration
class DatabaseConfig:
    def __init__(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.db_name = os.getenv("POSTGRES_DB")
        self.schema = os.getenv("POSTGRES_SCHEMA")
        self.ssl = os.getenv("POSTGRES_SSL", "false").lower() == "true"
        self.pool_size = int(os.getenv("POSTGRES_POOL_SIZE", "20"))

    @property
    def connection_string(self) -> str:
        return os.getenv("DATABASE_URL")


# Application configuration
class AppConfig:
    def __init__(self):
        self.env = os.getenv("APP_ENV", "development")
        self.debug = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.eth_rpc_url = os.getenv("ETH_RPC_URL")
        self.sync_blocks_count = int(os.getenv("SYNC_BLOCKS_COUNT", "10"))
        self.sync_interval = int(os.getenv("SYNC_INTERVAL", "12"))


# Blockchain sync state
class BlockchainSyncState:
    def __init__(self):
        self.last_synced_block = None
        self.is_syncing = False
        self.sync_start_time = None
        self.sync_end_time = None
        self.total_transactions = 0
        self.failed_transactions = 0


# Initialize configurations and state
db_config = DatabaseConfig()
app_config = AppConfig()
sync_state = BlockchainSyncState()


# Initialize FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await prisma.connect()
        logger.info("Successfully connected to database")

        # Get last synced block from database
        last_tx = await prisma.transaction.find_first(order={"blockNumber": "desc"})
        if last_tx:
            sync_state.last_synced_block = last_tx.blockNumber
            logger.info(
                f"Last synced block from database: {sync_state.last_synced_block}"
            )

        # Start blockchain sync scheduler
        scheduler.add_job(
            sync_blockchain_data, "interval", seconds=app_config.sync_interval
        )
        scheduler.start()
        logger.info(
            f"Blockchain sync scheduler started with {app_config.sync_interval}s interval"
        )
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise e

    yield

    # Shutdown
    try:
        scheduler.shutdown()
        logger.info("Scheduler shutdown complete")
        await prisma.disconnect()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


app = FastAPI(lifespan=lifespan)
prisma = Prisma()

# Initialize Web3 and scheduler
try:
    w3 = Web3(Web3.HTTPProvider(app_config.eth_rpc_url))
    if not w3.is_connected():
        raise Exception("Failed to connect to Ethereum node")
    logger.info("Successfully connected to Ethereum node")
except Exception as e:
    logger.error(f"Error connecting to Ethereum node: {str(e)}")
    raise e

scheduler = AsyncIOScheduler()


class TransactionResponse(BaseModel):
    id: int
    hash: str
    blockNumber: int
    fromAddr: str
    to: str
    value: str
    gasPrice: str
    gas: str
    timestamp: datetime
    status: bool
    createdAt: datetime
    updatedAt: datetime


class SyncStatus(BaseModel):
    is_syncing: bool
    last_synced_block: Optional[int]
    latest_network_block: int
    sync_start_time: Optional[datetime]
    sync_end_time: Optional[datetime]
    total_transactions: int
    failed_transactions: int
    blocks_behind: Optional[int]


async def process_transaction(tx_hash: str, block_timestamp: int) -> bool:
    try:
        # Get full transaction
        tx = w3.eth.get_transaction(tx_hash)
        # Get transaction receipt
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        # Create transaction record
        await prisma.transaction.create(
            data={
                "hash": tx_hash,
                "blockNumber": tx.blockNumber,
                "fromAddr": tx["from"],
                "to": tx.to if tx.to else "",
                "value": str(tx.value),
                "gasPrice": str(tx.gasPrice),
                "gas": str(tx.gas),
                "timestamp": datetime.fromtimestamp(block_timestamp),
                "status": receipt.status == 1,
            }
        )
        return True
    except Exception as e:
        logger.error(f"Error processing transaction {tx_hash}: {str(e)}")
        return False


async def sync_blockchain_data():
    if sync_state.is_syncing:
        logger.warning("Sync already in progress, skipping...")
        return

    try:
        sync_state.is_syncing = True
        sync_state.sync_start_time = datetime.utcnow()
        sync_state.total_transactions = 0
        sync_state.failed_transactions = 0

        # Get latest block number
        latest_block = w3.eth.block_number

        # Determine start block
        start_block = (
            sync_state.last_synced_block + 1
            if sync_state.last_synced_block
            else latest_block - app_config.sync_blocks_count
        )

        # Don't sync more than sync_blocks_count blocks at once
        end_block = min(latest_block, start_block + app_config.sync_blocks_count)

        logger.info(f"Starting sync from block {start_block} to {end_block}")

        for block_number in range(start_block, end_block + 1):
            try:
                # Get block with transactions
                block = w3.eth.get_block(block_number, full_transactions=True)

                # Process all transactions in block
                for tx in block.transactions:
                    tx_hash = tx.hash.hex()

                    # Check if transaction already exists
                    existing_tx = await prisma.transaction.find_unique(
                        where={"hash": tx_hash}
                    )

                    if not existing_tx:
                        success = await process_transaction(tx_hash, block.timestamp)
                        if success:
                            sync_state.total_transactions += 1
                        else:
                            sync_state.failed_transactions += 1

                sync_state.last_synced_block = block_number
                logger.info(
                    f"Synced block {block_number} with {len(block.transactions)} transactions"
                )

            except BlockNotFound:
                logger.warning(f"Block {block_number} not found, skipping...")
                continue
            except Exception as e:
                logger.error(f"Error processing block {block_number}: {str(e)}")
                continue

        sync_state.sync_end_time = datetime.utcnow()
        logger.info(
            f"Sync completed. Processed {sync_state.total_transactions} transactions with {sync_state.failed_transactions} failures"
        )

    except Exception as e:
        logger.error(f"Error during blockchain sync: {str(e)}")
    finally:
        sync_state.is_syncing = False


@app.get("/sync/status", response_model=SyncStatus)
async def get_sync_status():
    try:
        latest_block = w3.eth.block_number
        blocks_behind = latest_block - (sync_state.last_synced_block or latest_block)

        return SyncStatus(
            is_syncing=sync_state.is_syncing,
            last_synced_block=sync_state.last_synced_block,
            latest_network_block=latest_block,
            sync_start_time=sync_state.sync_start_time,
            sync_end_time=sync_state.sync_end_time,
            total_transactions=sync_state.total_transactions,
            failed_transactions=sync_state.failed_transactions,
            blocks_behind=blocks_behind,
        )
    except Exception as e:
        logger.error(f"Error getting sync status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get sync status")


@app.post("/sync/trigger")
async def trigger_sync():
    try:
        await sync_blockchain_data()
        return {"message": "Sync triggered successfully"}
    except Exception as e:
        logger.error(f"Error triggering sync: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to trigger sync")


@app.get("/health")
async def health_check():
    try:
        # Check database connection
        await prisma.transaction.count()
        # Check Ethereum node connection
        eth_syncing = w3.eth.syncing
        latest_block = w3.eth.block_number

        return {
            "status": "healthy",
            "database": "connected",
            "ethereum_node": {
                "connected": True,
                "syncing": eth_syncing,
                "latest_block": latest_block,
            },
            "sync_state": {
                "is_syncing": sync_state.is_syncing,
                "last_synced_block": sync_state.last_synced_block,
                "total_transactions": sync_state.total_transactions,
            },
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/transactions/", response_model=List[TransactionResponse])
async def get_transactions(skip: int = 0, limit: int = 10):
    try:
        transactions = await prisma.transaction.find_many(
            skip=skip, take=limit, order={"blockNumber": "desc"}
        )
        return transactions
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/transactions/{tx_hash}", response_model=TransactionResponse)
async def get_transaction(tx_hash: str):
    try:
        transaction = await prisma.transaction.find_unique(where={"hash": tx_hash})
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching transaction {tx_hash}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/transactions/block/{block_number}", response_model=List[TransactionResponse])
async def get_transactions_by_block(block_number: int):
    try:
        transactions = await prisma.transaction.find_many(
            where={"blockNumber": block_number}
        )
        return transactions
    except Exception as e:
        logger.error(f"Error fetching transactions for block {block_number}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=8000, log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
