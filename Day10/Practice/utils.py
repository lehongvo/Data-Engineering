#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml
import logging
import os
from logging.handlers import RotatingFileHandler
from web3 import Web3
from web3.exceptions import BlockNotFound, TransactionNotFound
import os
from dotenv import load_dotenv

# Đảm bảo biến môi trường được load
load_dotenv()

def setup_logging(name, log_level=logging.INFO, console_output=True):
    """
    Set up logging configuration with file output to logs directory.
    
    Args:
        name (str): Logger name
        log_level (int): Logging level
        console_output (bool): Whether to also output to console
    
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Add file handler with rotation (max 10MB per file, keep 5 backup files)
    log_file = os.path.join(log_dir, f"{name}.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

def load_config():
    """Load configuration from YAML file."""
    try:
        with open('config.yml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        raise

def get_web3_provider():
    """Get Web3 provider from configuration or environment variables."""
    # Ưu tiên biến môi trường
    provider_url = os.getenv('ETH_PROVIDER_URL')
    
    if not provider_url:
        # Nếu không có, sử dụng từ config
        config = load_config()
        default_provider = config['ethereum'].get('default_provider', 'llamarpc')
        
        # Sử dụng nhà cung cấp mặc định từ config
        if default_provider in config['ethereum']['providers']:
            provider_url = config['ethereum']['providers'][default_provider]
        else:
            # Fallback to LlamaRPC nếu không có mặc định
            provider_url = "https://eth.llamarpc.com"
        
        logging.info(f"Using Ethereum provider: {default_provider} at {provider_url}")
    else:
        logging.info(f"Using Ethereum provider from environment: {provider_url}")
    
    return Web3(Web3.HTTPProvider(provider_url))

def format_block_data(block):
    """Format block data to be JSON serializable."""
    return {
        'number': block.number,
        'hash': block.hash.hex(),
        'parent_hash': block.parentHash.hex(),
        'timestamp': block.timestamp,
        'gas_used': block.gasUsed,
        'gas_limit': block.gasLimit,
        'transaction_count': len(block.transactions),
        'miner': block.miner,
        'difficulty': block.difficulty,
        'total_difficulty': block.get('totalDifficulty', 0),
        'size': block.size,
        'nonce': block.nonce.hex(),
        'base_fee_per_gas': block.get('baseFeePerGas', 0),
    }

def format_transaction_data(tx, w3):
    """Format transaction data to be JSON serializable and add derived fields."""
    # Convert Decimal values to float for JSON serialization
    value_in_ether = w3.from_wei(tx['value'], 'ether')
    gas_price_in_gwei = w3.from_wei(tx['gasPrice'], 'gwei') if 'gasPrice' in tx else None
    
    return {
        'hash': tx['hash'].hex(),
        'block_number': tx['blockNumber'],
        'block_hash': tx['blockHash'].hex(),
        'from': tx['from'],
        'to': tx['to'] if tx['to'] else None,  # Contract creation
        'value': float(value_in_ether),  # Convert Decimal to float
        'value_wei': int(tx['value']),   # Convert to int to ensure serializable
        'gas': tx['gas'],
        'gas_price': float(gas_price_in_gwei) if gas_price_in_gwei is not None else None,  # Convert Decimal to float
        'nonce': tx['nonce'],
        'input_data': tx['input'],
        'transaction_index': tx['transactionIndex'],
        'is_contract_creation': tx['to'] is None,
        'is_contract_call': tx['input'] != '0x',
    }

def is_contract_address(address, w3):
    """Check if an address is a contract."""
    if not address:
        return False
    
    try:
        code = w3.eth.get_code(address)
        return code != b''
    except Exception:
        return False 