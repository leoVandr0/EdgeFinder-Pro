from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.services.user_store import WatchlistStore
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/api/watchlist", tags=["Watchlist"])


class AddPairRequest(BaseModel):
    pair: str


class WatchlistResponse(BaseModel):
    pairs: List[str]
    total: int


@router.get("/", response_model=WatchlistResponse)
async def get_watchlist(current_user: dict = Depends(get_current_user)):
    """
    Get user's watchlist

    Requires: Bearer token in Authorization header
    """
    pairs = WatchlistStore.get_watchlist(current_user["id"])

    return {
        "pairs": pairs,
        "total": len(pairs)
    }


@router.post("/", response_model=WatchlistResponse)
async def add_to_watchlist(
    request: AddPairRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Add a currency pair to watchlist

    - **pair**: Currency pair (e.g., EUR/USD, EURUSD, GBP/JPY)
    """
    # Normalize pair format
    pair = request.pair.upper().replace("-", "/")

    # Validate pair format
    if "/" in pair:
        parts = pair.split("/")
        if len(parts) != 2 or len(parts[0]) != 3 or len(parts[1]) != 3:
            raise HTTPException(status_code=400, detail="Invalid pair format. Use EUR/USD or EURUSD")
    elif len(pair) == 6:
        # Convert EURUSD to EUR/USD
        pair = f"{pair[:3]}/{pair[3:]}"
    else:
        raise HTTPException(status_code=400, detail="Invalid pair format. Use EUR/USD or EURUSD")

    pairs = WatchlistStore.add_to_watchlist(current_user["id"], pair)

    return {
        "pairs": pairs,
        "total": len(pairs)
    }


@router.delete("/{pair}", response_model=WatchlistResponse)
async def remove_from_watchlist(
    pair: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Remove a currency pair from watchlist

    - **pair**: Currency pair to remove (e.g., EUR/USD, EURUSD)
    """
    # Normalize pair format
    pair = pair.upper().replace("-", "/")

    if "/" not in pair and len(pair) == 6:
        pair = f"{pair[:3]}/{pair[3:]}"

    pairs = WatchlistStore.remove_from_watchlist(current_user["id"], pair)

    return {
        "pairs": pairs,
        "total": len(pairs)
    }


@router.delete("/", response_model=WatchlistResponse)
async def clear_watchlist(current_user: dict = Depends(get_current_user)):
    """
    Clear entire watchlist
    """
    WatchlistStore.clear_watchlist(current_user["id"])

    return {
        "pairs": [],
        "total": 0
    }
