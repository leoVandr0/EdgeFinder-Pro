from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Event(BaseModel):
    """Economic calendar event model"""
    id: Optional[str] = Field(None, alias="_id")
    currency: str = Field(..., description="Currency code (USD, EUR, etc.)")
    event_name: str = Field(..., description="Event title")
    impact: str = Field(..., description="High, Medium, Low")
    actual: Optional[str] = Field(None, description="Actual value")
    forecast: Optional[str] = Field(None, description="Forecast value")
    previous: Optional[str] = Field(None, description="Previous value")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "currency": "USD",
                "event_name": "Non-Farm Payrolls",
                "impact": "High",
                "actual": "250K",
                "forecast": "200K",
                "previous": "180K",
                "timestamp": "2025-10-20T14:30:00Z"
            }
        }
