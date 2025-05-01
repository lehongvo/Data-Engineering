#!/usr/bin/env python3

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine
import sqlalchemy as sa

# Add parent directory to path for importing the db_handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_handler import get_token_data

app = FastAPI(
    title="Token Data API",
    description="API to access token data collected from tama.meme",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Token Data API",
        "version": "1.0.0",
        "endpoints": {
            "tokens": "/api/tokens",
            "token_by_address": "/api/tokens/address/{address}",
            "health": "/api/health",
            "db_status": "/api/db-status",
        },
    }


@app.get("/api/tokens", tags=["Tokens"])
async def get_tokens(
    limit: int = Query(100, description="Number of tokens to return"),
    offset: int = Query(0, description="Number of tokens to skip"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_direction: str = Query("desc", description="Sort direction (asc/desc)"),
) -> Dict[str, Any]:
    """
    Get a list of tokens with pagination and sorting.
    """
    tokens = get_token_data(
        db_url="postgresql://kestra:k3str4@localhost:5432/kestra",
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )

    return {
        "status": "success",
        "count": len(tokens),
        "offset": offset,
        "limit": limit,
        "data": tokens,
    }


@app.get("/api/tokens/address/{address}", tags=["Tokens"])
async def get_token_by_address(address: str) -> Dict[str, Any]:
    """
    Get token details by address.
    """
    tokens = get_token_data(
        db_url="postgresql://kestra:k3str4@localhost:5432/kestra",
        limit=1,
        offset=0,
        sort_by="fetch_time",
        sort_direction="desc",
    )

    # Filter by address (case insensitive)
    token = next((t for t in tokens if t["address"].lower() == address.lower()), None)

    if not token:
        raise HTTPException(
            status_code=404, detail=f"Token with address {address} not found"
        )

    return {"status": "success", "data": token}


@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "message": "API is up and running"}


@app.get("/api/db-status", tags=["Health"])
async def db_status():
    """
    Check database connection status.
    """
    try:
        # Try connecting to the database
        db_url = "postgresql://kestra:k3str4@localhost:5432/kestra"
        engine = create_engine(db_url)

        # Execute simple query to check connection
        with engine.connect() as conn:
            result = conn.execute(sa.text("SELECT 1")).fetchone()

            # Check if table exists
            table_exists = conn.execute(
                sa.text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tokens')"
                )
            ).scalar()

            # Count records in tokens table if it exists
            record_count = 0
            if table_exists:
                record_count = conn.execute(
                    sa.text("SELECT COUNT(*) FROM tokens")
                ).scalar()

        return {
            "status": "connected",
            "message": "Database connection successful",
            "db_url": db_url.replace("kestra:k3str4", "kestra:****"),  # Hide password
            "table_exists": table_exists,
            "record_count": record_count,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "error_type": str(type(e).__name__),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
