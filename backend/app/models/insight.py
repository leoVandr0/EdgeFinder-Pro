from pydantic import BaseModel, Field
from typing import Optional

class Insight(BaseModel):
    """Trading insight/signal model"""
    id: Optional[int] = None
    pair: str = Field(..., description="Currency pair (e.g., EUR/USD)")
    signal_type: str = Field(..., description="buy, sell, hold")
    confidence: float = Field(..., ge=0, le=100, description="Confidence 0-100")
    entry_price: float = Field(..., description="Suggested entry price")
    stop_loss: float = Field(..., description="Stop loss level")
    take_profit: float = Field(..., description="Take profit target")
    reasoning: str = Field(..., description="AI-generated reasoning")
    timeframe: str = Field(default="H4", description="Timeframe (H1, H4, D1)")

    class Config:
        json_schema_extra = {
            "example": {
                "pair": "EUR/USD",
                "signal_type": "buy",
                "confidence": 82.5,
                "entry_price": 1.0950,
                "stop_loss": 1.0900,
                "take_profit": 1.1050,
                "reasoning": "Strong USD weakness combined with positive EU data",
                "timeframe": "H4"
            }
        }
