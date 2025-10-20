from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.event import Event

router = APIRouter(prefix="/api/events", tags=["Economic Calendar"])

# Sample economic events (in production, fetch from ForexFactory, Investing.com, etc.)
SAMPLE_EVENTS = [
    {
        "currency": "USD",
        "event_name": "Non-Farm Payrolls",
        "impact": "High",
        "actual": "250K",
        "forecast": "200K",
        "previous": "180K",
        "timestamp": datetime.utcnow() + timedelta(days=2)
    },
    {
        "currency": "EUR",
        "event_name": "ECB Interest Rate Decision",
        "impact": "High",
        "actual": None,
        "forecast": "4.50%",
        "previous": "4.25%",
        "timestamp": datetime.utcnow() + timedelta(days=5)
    },
    {
        "currency": "GBP",
        "event_name": "UK GDP Growth Rate",
        "impact": "High",
        "actual": "0.3%",
        "forecast": "0.2%",
        "previous": "0.1%",
        "timestamp": datetime.utcnow() - timedelta(days=1)
    },
    {
        "currency": "JPY",
        "event_name": "BoJ Monetary Policy Statement",
        "impact": "High",
        "actual": None,
        "forecast": None,
        "previous": None,
        "timestamp": datetime.utcnow() + timedelta(days=7)
    },
    {
        "currency": "USD",
        "event_name": "Consumer Price Index (CPI)",
        "impact": "High",
        "actual": "3.2%",
        "forecast": "3.0%",
        "previous": "2.9%",
        "timestamp": datetime.utcnow() - timedelta(hours=6)
    },
    {
        "currency": "EUR",
        "event_name": "German Manufacturing PMI",
        "impact": "Medium",
        "actual": "48.5",
        "forecast": "49.0",
        "previous": "49.2",
        "timestamp": datetime.utcnow() + timedelta(days=1)
    },
    {
        "currency": "AUD",
        "event_name": "RBA Interest Rate Decision",
        "impact": "High",
        "actual": None,
        "forecast": "4.35%",
        "previous": "4.10%",
        "timestamp": datetime.utcnow() + timedelta(days=3)
    },
    {
        "currency": "CAD",
        "event_name": "Employment Change",
        "impact": "Medium",
        "actual": "25K",
        "forecast": "20K",
        "previous": "15K",
        "timestamp": datetime.utcnow() - timedelta(days=2)
    },
    {
        "currency": "USD",
        "event_name": "FOMC Meeting Minutes",
        "impact": "High",
        "actual": None,
        "forecast": None,
        "previous": None,
        "timestamp": datetime.utcnow() + timedelta(days=10)
    },
    {
        "currency": "CHF",
        "event_name": "SNB Quarterly Assessment",
        "impact": "Medium",
        "actual": None,
        "forecast": None,
        "previous": None,
        "timestamp": datetime.utcnow() + timedelta(days=14)
    }
]

@router.get("/", response_model=List[Event])
async def get_economic_events(
    currency: Optional[str] = Query(None, description="Filter by currency code"),
    impact: Optional[str] = Query(None, description="Filter by impact level (High, Medium, Low)"),
    upcoming: bool = Query(True, description="Show only upcoming events")
):
    """
    Get economic calendar events.

    Returns scheduled and past economic events that impact currency markets:
    - Central bank decisions
    - Economic indicators (GDP, CPI, Employment)
    - Policy announcements
    """
    try:
        events = SAMPLE_EVENTS.copy()

        # Filter by currency
        if currency:
            currency = currency.upper()
            events = [e for e in events if e["currency"] == currency]

        # Filter by impact
        if impact:
            impact = impact.capitalize()
            events = [e for e in events if e["impact"] == impact]

        # Filter upcoming/past
        now = datetime.utcnow()
        if upcoming:
            events = [e for e in events if e["timestamp"] > now]
        else:
            events = [e for e in events if e["timestamp"] <= now]

        # Sort by timestamp
        events.sort(key=lambda x: x["timestamp"])

        return [Event(**event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")

@router.get("/today", response_model=List[Event])
async def get_todays_events():
    """Get all economic events scheduled for today"""
    try:
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        events = [
            e for e in SAMPLE_EVENTS
            if today_start <= e["timestamp"] < today_end
        ]

        events.sort(key=lambda x: x["timestamp"])
        return [Event(**event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/high-impact", response_model=List[Event])
async def get_high_impact_events():
    """Get only high-impact events"""
    try:
        events = [e for e in SAMPLE_EVENTS if e["impact"] == "High"]
        events.sort(key=lambda x: x["timestamp"])
        return [Event(**event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
