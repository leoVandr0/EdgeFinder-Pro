from fastapi import APIRouter, HTTPException
from app.services.indices_data import get_real_indices_data, get_real_index_data

router = APIRouter(prefix="/api/indices", tags=["Market Indices"])

@router.get("/")
async def get_all_indices():
    """
    Get real-time data for all major stock indices.

    Returns current price, change, and percentage change for:
    - NASDAQ Composite
    - Dow Jones Industrial Average (US30)
    - S&P 500
    - FTSE 100
    - DAX
    - Nikkei 225
    """
    try:
        indices_data = await get_real_indices_data()
        return {
            "indices": indices_data,
            "total": len(indices_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching indices data: {str(e)}")

@router.get("/{index_key}")
async def get_index(index_key: str):
    """
    Get real-time data for a specific index.

    Supported indices:
    - NASDAQ: NASDAQ Composite
    - US30: Dow Jones Industrial Average
    - SP500: S&P 500
    - FTSE100: FTSE 100
    - DAX: German DAX
    - NIKKEI: Nikkei 225
    """
    try:
        index_data = await get_real_index_data(index_key)

        if not index_data:
            raise HTTPException(
                status_code=404,
                detail=f"Index '{index_key}' not found. Supported: NASDAQ, US30, SP500, FTSE100, DAX, NIKKEI"
            )

        return index_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching index data: {str(e)}")
