"""
Real Forex Data Integration
Fetches live forex rates and calculates currency strength similar to EdgeFinder
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from collections import defaultdict

class ForexDataProvider:
    """
    Fetch real-time forex data from multiple sources
    Similar to EdgeFinder's methodology
    """

    def __init__(self):
        # API keys (set in environment variables)
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        self.exchange_rate_api_key = os.getenv("EXCHANGE_RATE_API_KEY", "")

        # Major currencies to track
        self.major_currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD"]

        # Cache for rates (updates every 15 minutes like EdgeFinder)
        self.rates_cache = {}
        self.cache_timestamp = None
        self.cache_duration = timedelta(minutes=15)

    async def get_forex_rates(self) -> Dict[str, float]:
        """
        Get real-time forex exchange rates
        Returns dict of currency pairs to rates (e.g., {"EUR/USD": 1.0850})
        """
        # Check cache first
        if self.cache_timestamp and (datetime.utcnow() - self.cache_timestamp) < self.cache_duration:
            return self.rates_cache

        rates = {}

        # Try exchangerate-api.com (free, no key required for basic tier)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Get USD as base
                response = await client.get("https://open.er-api.com/v6/latest/USD")
                if response.status_code == 200:
                    data = response.json()
                    usd_rates = data.get("rates", {})

                    # Calculate all major pairs
                    for base in self.major_currencies:
                        for quote in self.major_currencies:
                            if base != quote:
                                # Convert through USD if needed
                                if base == "USD":
                                    rate = usd_rates.get(quote, 1.0)
                                elif quote == "USD":
                                    rate = 1.0 / usd_rates.get(base, 1.0) if usd_rates.get(base) else 1.0
                                else:
                                    # Cross rate: base/quote = (USD/quote) / (USD/base)
                                    quote_rate = usd_rates.get(quote, 1.0)
                                    base_rate = usd_rates.get(base, 1.0)
                                    rate = quote_rate / base_rate if base_rate else 1.0

                                pair = f"{base}/{quote}"
                                rates[pair] = round(rate, 5)

                    # Update cache
                    self.rates_cache = rates
                    self.cache_timestamp = datetime.utcnow()
                    return rates
        except Exception as e:
            print(f"Error fetching forex rates: {e}")

        # Fallback to cached data if available
        if self.rates_cache:
            return self.rates_cache

        # Last resort: return empty dict
        return {}

    def calculate_currency_strength_from_rates(self, rates: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate currency strength scores from exchange rates
        EdgeFinder methodology: aggregate performance vs all other currencies

        Returns: Dict of currency -> strength score (0-100)
        """
        if not rates:
            return {}

        # Calculate raw strength for each currency
        currency_strength = defaultdict(float)
        pair_count = defaultdict(int)

        for pair, rate in rates.items():
            if "/" not in pair:
                continue

            base, quote = pair.split("/")

            # Base currency gains strength when rate increases
            # Quote currency loses strength when rate increases
            # Normalize rate change to percentage

            # Use rate deviation from 1.0 as strength indicator
            if rate > 1.0:
                # Base is stronger
                currency_strength[base] += (rate - 1.0) * 10
                currency_strength[quote] -= (rate - 1.0) * 10
            else:
                # Quote is stronger
                currency_strength[quote] += (1.0 - rate) * 10
                currency_strength[base] -= (1.0 - rate) * 10

            pair_count[base] += 1
            pair_count[quote] += 1

        # Average and normalize to 0-100 scale
        normalized_strength = {}
        for currency in self.major_currencies:
            if pair_count[currency] > 0:
                avg_strength = currency_strength[currency] / pair_count[currency]
                # Normalize to 0-100 (assuming typical range is -50 to +50)
                normalized = 50 + avg_strength
                normalized = max(0, min(100, normalized))  # Clamp to 0-100
                normalized_strength[currency] = round(normalized, 2)
            else:
                normalized_strength[currency] = 50.0  # Neutral

        return normalized_strength

    async def get_currency_strength(self) -> Dict[str, float]:
        """
        Get real-time currency strength scores
        Similar to EdgeFinder's currency strength meter
        """
        rates = await self.get_forex_rates()
        return self.calculate_currency_strength_from_rates(rates)


# Singleton instance
forex_provider = ForexDataProvider()


async def get_real_currency_strength() -> Dict[str, float]:
    """
    Get real currency strength scores
    Call this from your analytics service
    """
    return await forex_provider.get_currency_strength()


async def get_real_forex_rates() -> Dict[str, float]:
    """
    Get real forex exchange rates
    """
    return await forex_provider.get_forex_rates()


async def get_real_forex_price(base: str, quote: str) -> Optional[float]:
    """
    Get real forex price for a currency pair (e.g., EUR/USD)
    Returns the current exchange rate from base to quote currency
    """
    try:
        rates = await forex_provider.get_forex_rates()
        pair = f"{base}/{quote}"
        return rates.get(pair)
    except Exception as e:
        print(f"Error getting forex price for {base}/{quote}: {e}")
        return None
