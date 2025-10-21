import random
import asyncio
from datetime import datetime
from typing import Dict
from app.models.strength import CurrencyStrength, StrengthResponse

# Major currency pairs
MAJOR_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD"]

# Cache for storing previous strength values to calculate momentum
_previous_strengths = {}
_use_real_data = True  # Toggle to switch between real and demo data


async def calculate_currency_strength_async() -> StrengthResponse:
    """
    Calculate weighted currency strength using REAL forex data.
    Similar to EdgeFinder's methodology.
    """
    global _previous_strengths

    try:
        if _use_real_data:
            # Import here to avoid circular imports
            from app.services.forex_data import get_real_currency_strength

            # Get real currency strength scores
            strength_scores = await get_real_currency_strength()

            if not strength_scores:
                # Fallback to demo data if API fails
                return _calculate_demo_strength()

        else:
            # Use demo data
            return _calculate_demo_strength()

    except Exception as e:
        print(f"Error calculating real strength: {e}")
        return _calculate_demo_strength()

    strengths = {}

    # Sort by score to assign ranks
    sorted_currencies = sorted(strength_scores.items(), key=lambda x: x[1], reverse=True)

    for rank, (currency, score) in enumerate(sorted_currencies, 1):
        # Calculate momentum by comparing to previous strength
        previous_score = _previous_strengths.get(currency, score)
        momentum = score - previous_score

        # Store current score for next calculation
        _previous_strengths[currency] = score

        # Determine trend based on momentum
        if momentum > 1.5:
            trend = "bullish"
        elif momentum < -1.5:
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


def calculate_currency_strength() -> StrengthResponse:
    """
    Synchronous wrapper for async currency strength calculation
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create new task
            return asyncio.run(calculate_currency_strength_async())
        else:
            return loop.run_until_complete(calculate_currency_strength_async())
    except Exception as e:
        print(f"Error in sync wrapper: {e}")
        return _calculate_demo_strength()


def _calculate_demo_strength() -> StrengthResponse:
    """
    Fallback demo data when real data is unavailable
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

async def calculate_pair_comparison(base: str, quote: str) -> Dict:
    """
    Compare two currencies in a pair (e.g., EUR vs USD in EUR/USD).
    Returns relative strength, divergence, and recommended action.
    """
    strength_data = await calculate_currency_strength_async()

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

async def generate_trade_insights(limit: int = 10) -> list:
    """
    Generate top trading insights based on currency strength divergence.
    Returns list of high-confidence trade signals.
    """
    strength_data = await calculate_currency_strength_async()
    insights = []

    # Generate insights for major pairs
    major_pairs = [
        ("EUR", "USD"), ("GBP", "USD"), ("USD", "JPY"),
        ("AUD", "USD"), ("USD", "CAD"), ("USD", "CHF"),
        ("EUR", "GBP"), ("EUR", "JPY"), ("GBP", "JPY"),
        ("AUD", "JPY")
    ]

    for base, quote in major_pairs:
        comparison = await calculate_pair_comparison(base, quote)

        if comparison.get("confidence", 0) > 60:
            # Get real forex price
            if _use_real_data:
                from app.services.forex_data import get_real_forex_price
                real_price = await get_real_forex_price(base, quote)
                if real_price is None:
                    continue  # Skip if we can't get real price
                entry = round(real_price, 4)
            else:
                # Fallback to simulated price
                entry = round(random.uniform(0.8, 1.5), 4)

            signal_type = "buy" if comparison["recommendation"] in ["Buy", "Strong Buy"] else "sell"

            # Calculate stop loss and take profit based on real price
            # Use typical forex risk management: 1.5% stop loss, 2.5% take profit for buys
            # Reverse for sells
            if signal_type == "buy":
                stop_loss = round(entry * 0.985, 4)  # 1.5% below entry
                take_profit = round(entry * 1.025, 4)  # 2.5% above entry
            else:
                stop_loss = round(entry * 1.015, 4)  # 1.5% above entry
                take_profit = round(entry * 0.975, 4)  # 2.5% below entry

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
