from fastapi import APIRouter, HTTPException, Query
from app.services.analytics import calculate_pair_comparison

router = APIRouter(prefix="/api/pair-compare", tags=["Pair Comparison"])

@router.get("/")
async def compare_currency_pair(
    base: str = Query(..., description="Base currency (e.g., EUR)"),
    quote: str = Query(..., description="Quote currency (e.g., USD)")
):
    """
    Compare two currencies in a pair and get trading recommendations.

    Analyzes the relative strength between base and quote currencies:
    - Strength divergence calculation
    - Trend alignment
    - Entry/exit recommendations
    - Confidence scoring

    Example: /api/pair-compare?base=EUR&quote=USD
    """
    try:
        base = base.upper()
        quote = quote.upper()

        if len(base) != 3 or len(quote) != 3:
            raise HTTPException(status_code=400, detail="Currency codes must be 3 characters")

        result = await calculate_pair_comparison(base, quote)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing pair: {str(e)}")

@router.get("/{pair}")
async def compare_pair_direct(pair: str):
    """
    Compare currency pair using direct pair notation (e.g., EUR/USD or EURUSD).
    """
    try:
        # Parse pair format
        pair = pair.upper().replace("-", "/")

        if "/" in pair:
            parts = pair.split("/")
            if len(parts) != 2:
                raise HTTPException(status_code=400, detail="Invalid pair format")
            base, quote = parts
        elif len(pair) == 6:
            base = pair[:3]
            quote = pair[3:]
        else:
            raise HTTPException(status_code=400, detail="Invalid pair format. Use EUR/USD or EURUSD")

        result = await calculate_pair_comparison(base, quote)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
