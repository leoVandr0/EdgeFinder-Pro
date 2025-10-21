"""
Historical Price Data & Technical Indicators
Provides historical forex data with technical analysis indicators
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random


def generate_sample_ohlc_data(pair: str, days: int = 90) -> pd.DataFrame:
    """
    Generate sample OHLC (Open, High, Low, Close) data for demonstration
    In production, replace with real historical data from a forex data provider
    """
    # Base prices for major pairs
    base_prices = {
        "EUR/USD": 1.0850,
        "GBP/USD": 1.2650,
        "USD/JPY": 150.50,
        "AUD/USD": 0.6520,
        "USD/CAD": 1.3580,
        "USD/CHF": 0.8920,
        "EUR/GBP": 0.8575,
        "EUR/JPY": 163.25,
        "GBP/JPY": 190.40
    }

    base_price = base_prices.get(pair, 1.0)

    # Generate timestamps
    end_date = datetime.utcnow()
    dates = [end_date - timedelta(days=i) for i in range(days, -1, -1)]

    data = []
    current_price = base_price

    for date in dates:
        # Random walk with some volatility
        change = random.uniform(-0.015, 0.015)  # 1.5% max change
        current_price = current_price * (1 + change)

        # Generate OHLC
        open_price = current_price
        high_price = current_price * (1 + random.uniform(0, 0.008))
        low_price = current_price * (1 - random.uniform(0, 0.008))
        close_price = current_price * (1 + random.uniform(-0.005, 0.005))

        # Volume (random)
        volume = random.randint(100000, 500000)

        data.append({
            "timestamp": date,
            "open": round(open_price, 5),
            "high": round(high_price, 5),
            "low": round(low_price, 5),
            "close": round(close_price, 5),
            "volume": volume
        })

        current_price = close_price

    df = pd.DataFrame(data)
    df.set_index("timestamp", inplace=True)

    return df


def calculate_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """Calculate Simple Moving Average"""
    return data["close"].rolling(window=period).mean()


def calculate_ema(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """Calculate Exponential Moving Average"""
    return data["close"].ewm(span=period, adjust=False).mean()


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = data["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = data["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = data["close"].ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }


def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, std_dev: int = 2) -> Dict:
    """Calculate Bollinger Bands"""
    sma = data["close"].rolling(window=period).mean()
    std = data["close"].rolling(window=period).std()

    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)

    return {
        "upper": upper_band,
        "middle": sma,
        "lower": lower_band
    }


def get_historical_data_with_indicators(
    pair: str,
    days: int = 90,
    indicators: Optional[List[str]] = None
) -> Dict:
    """
    Get historical OHLC data with technical indicators

    Args:
        pair: Currency pair (e.g., "EUR/USD")
        days: Number of days of historical data
        indicators: List of indicators to calculate (sma, ema, rsi, macd, bollinger)

    Returns:
        Dictionary with OHLC data and calculated indicators
    """
    # Generate or fetch historical data
    df = generate_sample_ohlc_data(pair, days)

    # Prepare result
    result = {
        "pair": pair,
        "timeframe": "daily",
        "data": []
    }

    # Calculate requested indicators
    if indicators is None:
        indicators = ["sma", "ema", "rsi", "macd"]

    calculated_indicators = {}

    if "sma" in indicators or "sma20" in indicators:
        calculated_indicators["sma20"] = calculate_sma(df, 20)
    if "sma50" in indicators:
        calculated_indicators["sma50"] = calculate_sma(df, 50)

    if "ema" in indicators or "ema20" in indicators:
        calculated_indicators["ema20"] = calculate_ema(df, 20)
    if "ema50" in indicators:
        calculated_indicators["ema50"] = calculate_ema(df, 50)

    if "rsi" in indicators:
        calculated_indicators["rsi"] = calculate_rsi(df, 14)

    if "macd" in indicators:
        macd = calculate_macd(df)
        calculated_indicators["macd"] = macd["macd"]
        calculated_indicators["macd_signal"] = macd["signal"]
        calculated_indicators["macd_histogram"] = macd["histogram"]

    if "bollinger" in indicators:
        bb = calculate_bollinger_bands(df)
        calculated_indicators["bb_upper"] = bb["upper"]
        calculated_indicators["bb_middle"] = bb["middle"]
        calculated_indicators["bb_lower"] = bb["lower"]

    # Combine OHLC data with indicators
    for idx, row in df.iterrows():
        data_point = {
            "timestamp": idx.isoformat(),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"])
        }

        # Add indicator values
        for indicator_name, indicator_series in calculated_indicators.items():
            value = indicator_series.loc[idx]
            if pd.notna(value):
                data_point[indicator_name] = round(float(value), 5)
            else:
                data_point[indicator_name] = None

        result["data"].append(data_point)

    result["total_points"] = len(result["data"])

    return result
