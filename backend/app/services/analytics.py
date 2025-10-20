import random
from datetime import datetime
from typing import Dict
from app.models.strength import CurrencyStrength, StrengthResponse

# Major currency pairs
MAJOR_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD"]

def calculate_currency_strength() -> StrengthResponse:
    """
    Calculate weighted currency strength using fundamental and technical factors.
    In production, this would use real-time forex data, interest rates, GDP, etc.
    """
    strengths = {}

    # Simulate strength calculation with weighted factors
    base_scores = {
        "USD": 75.5 + random.uniform(-5, 5),
        "EUR": 68.2 + random.uniform(-5, 5),
        "GBP": 72.1 + random.uniform(-5, 5),
        "JPY": 64.3 + random.uniform(-5, 5),
        "CHF": 70.8 + random.uniform(-5, 5),
        "AUD": 66.5 + random.uniform(-5, 5),
        "CAD": 69.2 + random.uniform(-5, 5),
        "NZD": 63.7 + random.uniform(-5, 5),
    }

    # Sort by score to assign ranks
    sorted_currencies = sorted(base_scores.items(), key=lambda x: x[1], reverse=True)

    for rank, (currency, score) in enumerate(sorted_currencies, 1):
        # Calculate momentum (simulated)
        momentum = random.uniform(-3, 3)

        # Determine trend
        if momentum > 1:
            trend = "bullish"
        elif momentum < -1:
            trend = "bearish"
        else:
            trend = "neutral"

        strengths[currency] = CurrencyStrength(
            currency=currency,
            strength_score=round(score, 2),
            momentum=round(momentum, 2),
            trend=trend,
            rank=rank
        )

    return StrengthResponse(
        strengths=strengths,
        updated_at=datetime.utcnow().isoformat()
    )

def calculate_pair_comparison(base: str, quote: str) -> Dict:
    """
    Compare two currencies in a pair (e.g., EUR vs USD in EUR/USD).
    Returns relative strength, divergence, and recommended action.
    """
    strength_data = calculate_currency_strength()

    base_strength = strength_data.strengths.get(base.upper())
    quote_strength = strength_data.strengths.get(quote.upper())

    if not base_strength or not quote_strength:
        return {"error": "Invalid currency pair"}

    # Calculate divergence
    divergence = base_strength.strength_score - quote_strength.strength_score

    # Determine recommendation
    if divergence > 10:
        recommendation = "Strong Buy"
        confidence = min(95, 50 + abs(divergence) * 2)
    elif divergence > 5:
        recommendation = "Buy"
        confidence = min(85, 50 + abs(divergence) * 2)
    elif divergence < -10:
        recommendation = "Strong Sell"
        confidence = min(95, 50 + abs(divergence) * 2)
    elif divergence < -5:
        recommendation = "Sell"
        confidence = min(85, 50 + abs(divergence) * 2)
    else:
        recommendation = "Neutral"
        confidence = 50

    return {
        "pair": f"{base}/{quote}",
        "base_currency": {
            "currency": base_strength.currency,
            "strength": base_strength.strength_score,
            "momentum": base_strength.momentum,
            "trend": base_strength.trend,
            "rank": base_strength.rank
        },
        "quote_currency": {
            "currency": quote_strength.currency,
            "strength": quote_strength.strength_score,
            "momentum": quote_strength.momentum,
            "trend": quote_strength.trend,
            "rank": quote_strength.rank
        },
        "divergence": round(divergence, 2),
        "recommendation": recommendation,
        "confidence": round(confidence, 2),
        "analysis": f"{base} is {'stronger' if divergence > 0 else 'weaker'} than {quote} by {abs(round(divergence, 2))} points."
    }

def generate_trade_insights(limit: int = 10) -> list:
    """
    Generate top trading insights based on currency strength divergence.
    Returns list of high-confidence trade signals.
    """
    strength_data = calculate_currency_strength()
    insights = []

    # Generate insights for major pairs
    major_pairs = [
        ("EUR", "USD"), ("GBP", "USD"), ("USD", "JPY"),
        ("AUD", "USD"), ("USD", "CAD"), ("USD", "CHF"),
        ("EUR", "GBP"), ("EUR", "JPY"), ("GBP", "JPY"),
        ("AUD", "JPY")
    ]

    for base, quote in major_pairs:
        comparison = calculate_pair_comparison(base, quote)

        if comparison.get("confidence", 0) > 60:
            # Simulate price data
            base_price = round(random.uniform(0.8, 1.5), 4)

            signal_type = "buy" if comparison["recommendation"] in ["Buy", "Strong Buy"] else "sell"
            if signal_type == "buy":
                entry = base_price
                stop_loss = round(entry * 0.985, 4)
                take_profit = round(entry * 1.025, 4)
            else:
                entry = base_price
                stop_loss = round(entry * 1.015, 4)
                take_profit = round(entry * 0.975, 4)

            insights.append({
                "pair": comparison["pair"],
                "signal_type": signal_type,
                "confidence": comparison["confidence"],
                "entry_price": entry,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "reasoning": comparison["analysis"],
                "timeframe": "H4"
            })

    # Sort by confidence and return top insights
    insights.sort(key=lambda x: x["confidence"], reverse=True)
    return insights[:limit]
