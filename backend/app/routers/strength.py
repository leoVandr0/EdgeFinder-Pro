from fastapi import APIRouter, HTTPException
from app.services.analytics import calculate_currency_strength_async
from app.models.strength import StrengthResponse

router = APIRouter(prefix="/api/strength", tags=["Currency Strength"])

@router.get("/", response_model=StrengthResponse)
async def get_currency_strength():
    """
    Get current strength scores for all major currencies.

    Returns weighted strength scores (0-100) based on:
    - Technical momentum indicators
    - Fundamental economic data
    - Market sentiment
    """
    try:
        return await calculate_currency_strength_async()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating strength: {str(e)}")

@router.get("/currency/{currency_code}")
async def get_single_currency_strength(currency_code: str):
    """Get strength data for a specific currency"""
    try:
        data = await calculate_currency_strength_async()
        currency = currency_code.upper()

        if currency not in data.strengths:
            raise HTTPException(status_code=404, detail=f"Currency {currency} not found")

        return {
            "currency": currency,
            "data": data.strengths[currency],
            "updated_at": data.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
