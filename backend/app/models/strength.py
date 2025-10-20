from pydantic import BaseModel, Field
from typing import Dict

class CurrencyStrength(BaseModel):
    """Currency strength model with weighted scoring"""
    currency: str = Field(..., description="Currency code")
    strength_score: float = Field(..., ge=0, le=100, description="Strength score 0-100")
    momentum: float = Field(..., description="Recent momentum indicator")
    trend: str = Field(..., description="bullish, bearish, neutral")
    rank: int = Field(..., ge=1, description="Global rank")

    class Config:
        json_schema_extra = {
            "example": {
                "currency": "USD",
                "strength_score": 78.5,
                "momentum": 2.3,
                "trend": "bullish",
                "rank": 1
            }
        }

class StrengthResponse(BaseModel):
    """Response containing all currency strengths"""
    strengths: Dict[str, CurrencyStrength]
    updated_at: str
