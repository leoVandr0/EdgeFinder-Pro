from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.analytics import generate_trade_insights
from app.models.insight import Insight

router = APIRouter(prefix="/api/insights", tags=["Trading Insights"])

@router.get("/", response_model=List[Insight])
async def get_trade_insights(
    limit: int = Query(default=10, ge=1, le=50, description="Number of insights to return")
):
    """
    Get AI-generated trading insights and signals.

    Returns top trade opportunities ranked by confidence based on:
    - Currency strength divergence
    - Technical analysis
    - Fundamental factors
    - Risk-reward ratios
    """
    try:
        insights = await generate_trade_insights(limit=limit)
        return [Insight(**insight) for insight in insights]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@router.get("/pair/{pair}")
async def get_pair_insights(pair: str):
    """
    Get specific insights for a currency pair (e.g., EUR/USD).
    """
    try:
        # Normalize pair format
        pair = pair.upper().replace("-", "/")
        if "/" not in pair:
            # Assume 6-character format like EURUSD
            if len(pair) == 6:
                pair = f"{pair[:3]}/{pair[3:]}"
            else:
                raise HTTPException(status_code=400, detail="Invalid pair format")

        all_insights = await generate_trade_insights(limit=50)

        # Filter for specific pair
        pair_insights = [i for i in all_insights if i["pair"] == pair]

        if not pair_insights:
            raise HTTPException(status_code=404, detail=f"No insights found for {pair}")

        return [Insight(**insight) for insight in pair_insights]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
