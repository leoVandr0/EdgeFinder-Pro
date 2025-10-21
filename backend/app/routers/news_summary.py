from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from app.services.sentiment import generate_news_summary, analyze_news_sentiment

router = APIRouter(prefix="/api/news-summary", tags=["News & Sentiment"])

# Sample news articles (in production, fetch from news APIs)
SAMPLE_NEWS = [
    {
        "title": "Federal Reserve Signals Potential Rate Cut in Q4",
        "content": "The Federal Reserve indicated in today's meeting that interest rates may be reduced in the fourth quarter as inflation shows signs of cooling. Chair Powell emphasized data-dependent decision making while acknowledging improved economic conditions. Markets rallied on the dovish tone.",
        "source": "Reuters",
        "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        "url": "https://example.com/fed-rate-cut"
    },
    {
        "title": "European Central Bank Maintains Hawkish Stance",
        "content": "ECB President Lagarde reiterated the bank's commitment to fighting inflation, stating that rates will remain elevated for an extended period. The central bank raised its inflation forecast for 2025, citing persistent price pressures in the services sector.",
        "source": "Bloomberg",
        "timestamp": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
        "url": "https://example.com/ecb-hawkish"
    },
    {
        "title": "British Pound Surges on Positive GDP Data",
        "content": "The British pound gained significant ground against major currencies after the UK reported better-than-expected GDP growth of 0.3% in the latest quarter. Analysts are revising their forecasts upward as the economy shows robust recovery momentum.",
        "source": "Financial Times",
        "timestamp": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
        "url": "https://example.com/gbp-surge"
    },
    {
        "title": "Japanese Yen Weakens as BoJ Maintains Ultra-Loose Policy",
        "content": "The Bank of Japan held its ultra-accommodative monetary policy steady despite rising inflation concerns. Governor Ueda stated that wage growth must accelerate before policy normalization begins. The yen fell to multi-month lows against the dollar.",
        "source": "Nikkei",
        "timestamp": (datetime.utcnow() - timedelta(hours=12)).isoformat(),
        "url": "https://example.com/boj-policy"
    },
    {
        "title": "US Dollar Strengthens on Strong Employment Report",
        "content": "The US dollar rallied across the board following robust non-farm payrolls data that exceeded forecasts by 50,000 jobs. The unemployment rate dipped to 3.7%, reinforcing the Federal Reserve's position on maintaining restrictive policy for longer.",
        "source": "CNBC",
        "timestamp": (datetime.utcnow() - timedelta(hours=18)).isoformat(),
        "url": "https://example.com/usd-employment"
    },
    {
        "title": "Euro Falls on German Manufacturing Concerns",
        "content": "The euro declined sharply after Germany's manufacturing PMI dropped below expectations, signaling economic weakness in Europe's largest economy. Analysts express concern about the region's industrial outlook amid global trade tensions.",
        "source": "Wall Street Journal",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "url": "https://example.com/euro-manufacturing"
    },
    {
        "title": "Australian Dollar Gains on Commodity Price Rally",
        "content": "The Australian dollar strengthened as commodity prices surged, driven by strong Chinese demand and supply constraints. Iron ore and coal prices reached six-month highs, boosting optimism for Australia's export-driven economy.",
        "source": "Sydney Morning Herald",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=6)).isoformat(),
        "url": "https://example.com/aud-commodities"
    },
    {
        "title": "Canadian Dollar Under Pressure from Oil Price Decline",
        "content": "The Canadian dollar weakened as crude oil prices fell amid concerns about global demand. The Bank of Canada's recent rate hike has done little to support the currency as energy prices remain the dominant driver.",
        "source": "Globe and Mail",
        "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "url": "https://example.com/cad-oil"
    },
    {
        "title": "Swiss Franc Benefits from Safe-Haven Flows",
        "content": "The Swiss franc appreciated against major currencies as geopolitical tensions drove investors toward safe-haven assets. The SNB expressed concern about franc strength but refrained from intervention signals.",
        "source": "Neue Zürcher Zeitung",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=12)).isoformat(),
        "url": "https://example.com/chf-safe-haven"
    },
    {
        "title": "New Zealand Dollar Drops After RBNZ Dovish Comments",
        "content": "The New Zealand dollar tumbled after the Reserve Bank indicated that the tightening cycle may be complete. Officials pointed to cooling domestic demand and housing market weakness as justification for the pause.",
        "source": "New Zealand Herald",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "url": "https://example.com/nzd-rbnz"
    }
]

@router.get("/")
async def get_news_summaries(
    limit: int = Query(default=10, ge=1, le=50, description="Number of articles to return"),
    currency: Optional[str] = Query(None, description="Filter by currency mention")
):
    """
    Get real forex news with sentiment analysis from ForexFactory, Investing.com, and DailyFX.

    Returns:
    - Real news articles from live sources
    - Sentiment scoring (positive, neutral, negative)
    - Source and timestamp
    - Relevance to currency markets
    """
    # Import here to avoid circular imports
    from app.services.news_fetcher import get_real_forex_news

    # Get real news
    news = await get_real_forex_news(limit=limit * 2)  # Fetch more for filtering

    # Filter by currency if specified
    if currency:
        currency = currency.upper()
        news = [
            article for article in news
            if currency.lower() in article.get("title", "").lower() or
               currency.lower() in article.get("content", "").lower()
        ]

    # Limit results
    news = news[:limit]

    # Generate summaries with sentiment
    summaries = generate_news_summary(news, max_items=limit)

    return {
        "total": len(summaries),
        "articles": summaries
    }

@router.get("/sentiment")
async def get_overall_sentiment():
    """
    Get aggregated market sentiment from recent news.
    """
    try:
        sentiment_analysis = analyze_news_sentiment(SAMPLE_NEWS)
        return sentiment_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/currency/{currency_code}")
async def get_currency_news(
    currency_code: str,
    limit: int = Query(default=5, ge=1, le=20)
):
    """
    Get news articles specifically mentioning a currency.
    """
    try:
        currency = currency_code.upper()

        # Filter articles mentioning the currency
        relevant_news = [
            article for article in SAMPLE_NEWS
            if currency.lower() in article["title"].lower() or
               currency.lower() in article["content"].lower()
        ]

        if not relevant_news:
            return {
                "currency": currency,
                "total": 0,
                "articles": [],
                "message": f"No recent news found for {currency}"
            }

        summaries = generate_news_summary(relevant_news, max_items=limit)
        sentiment = analyze_news_sentiment(relevant_news)

        return {
            "currency": currency,
            "total": len(summaries),
            "articles": summaries,
            "sentiment": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
