from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.historical_data import get_historical_data_with_indicators

router = APIRouter(prefix="/api/charts", tags=["Charts & Technical Analysis"])


@router.get("/{pair}")
async def get_chart_data(
    pair: str,
    days: int = Query(default=90, ge=7, le=365, description="Number of days of historical data"),
    indicators: Optional[str] = Query(None, description="Comma-separated list of indicators (sma,ema,rsi,macd,bollinger)")
):
    """
    Get historical OHLC data with technical indicators for charting

    **Supported Indicators:**
    - **sma**: Simple Moving Average (20-day)
    - **sma50**: 50-day SMA
    - **ema**: Exponential Moving Average (20-day)
    - **ema50**: 50-day EMA
    - **rsi**: Relative Strength Index (14-day)
    - **macd**: MACD (12, 26, 9)
    - **bollinger**: Bollinger Bands (20-day, 2 std dev)

    **Example:**
    - `/api/charts/EUR/USD?days=90&indicators=sma,ema,rsi,macd`
    - `/api/charts/EURUSD?days=30&indicators=rsi,bollinger`
    """
    try:
        # Normalize pair format
        pair = pair.upper().replace("-", "/")

        if "/" not in pair:
            if len(pair) == 6:
                pair = f"{pair[:3]}/{pair[3:]}"
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid pair format. Use EUR/USD or EURUSD"
                )

        # Parse indicators
        indicator_list = []
        if indicators:
            indicator_list = [ind.strip().lower() for ind in indicators.split(",")]
        else:
            # Default indicators
            indicator_list = ["sma", "ema", "rsi", "macd"]

        # Get historical data with indicators
        data = get_historical_data_with_indicators(pair, days, indicator_list)

        return data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart data: {str(e)}")


@router.get("/{pair}/indicators")
async def get_available_indicators():
    """
    Get list of available technical indicators
    """
    return {
        "indicators": [
            {
                "name": "sma",
                "description": "Simple Moving Average (20-day)",
                "parameters": {"period": 20}
            },
            {
                "name": "sma50",
                "description": "Simple Moving Average (50-day)",
                "parameters": {"period": 50}
            },
            {
                "name": "ema",
                "description": "Exponential Moving Average (20-day)",
                "parameters": {"period": 20}
            },
            {
                "name": "ema50",
                "description": "Exponential Moving Average (50-day)",
                "parameters": {"period": 50}
            },
            {
                "name": "rsi",
                "description": "Relative Strength Index",
                "parameters": {"period": 14}
            },
            {
                "name": "macd",
                "description": "MACD",
                "parameters": {"fast": 12, "slow": 26, "signal": 9}
            },
            {
                "name": "bollinger",
                "description": "Bollinger Bands",
                "parameters": {"period": 20, "std_dev": 2}
            }
        ]
    }
