"""
Admin endpoints for testing and configuration
"""
from fastapi import APIRouter
from app.services import analytics
from app.services.forex_data import forex_provider

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/data-source")
async def get_data_source():
    """Check if using real or demo data"""
    return {
        "using_real_data": analytics._use_real_data,
        "cache_status": {
            "has_cached_rates": bool(forex_provider.rates_cache),
            "cache_timestamp": forex_provider.cache_timestamp.isoformat() if forex_provider.cache_timestamp else None,
            "cached_pairs_count": len(forex_provider.rates_cache)
        }
    }


@router.post("/toggle-data-source")
async def toggle_data_source():
    """Toggle between real and demo data"""
    analytics._use_real_data = not analytics._use_real_data
    return {
        "using_real_data": analytics._use_real_data,
        "message": f"Switched to {'REAL' if analytics._use_real_data else 'DEMO'} data"
    }


@router.get("/forex-rates")
async def get_current_forex_rates():
    """Get current cached forex rates"""
    from app.services.forex_data import get_real_forex_rates

    rates = await get_real_forex_rates()
    return {
        "total_pairs": len(rates),
        "sample_rates": dict(list(rates.items())[:10]),  # Show first 10 pairs
        "cache_timestamp": forex_provider.cache_timestamp.isoformat() if forex_provider.cache_timestamp else None
    }
