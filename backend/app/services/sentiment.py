import re
from typing import Dict, List
from datetime import datetime

# Keyword-based sentiment analysis (fallback when no AI API available)
POSITIVE_KEYWORDS = [
    "bullish", "rally", "surge", "gains", "growth", "rise", "improve",
    "strong", "robust", "recover", "optimistic", "boost", "advance", "climb"
]

NEGATIVE_KEYWORDS = [
    "bearish", "fall", "decline", "drop", "weak", "plunge", "crash",
    "concern", "risk", "fears", "uncertainty", "slump", "tumble", "pessimistic"
]

def analyze_sentiment_fallback(text: str) -> Dict:
    """
    Fallback sentiment analyzer using keyword matching.
    Returns sentiment score from -1 (negative) to 1 (positive).
    """
    text_lower = text.lower()

    positive_count = sum(1 for word in POSITIVE_KEYWORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_KEYWORDS if word in text_lower)

    total = positive_count + negative_count
    if total == 0:
        score = 0
        label = "neutral"
    else:
        score = (positive_count - negative_count) / max(total, 1)
        if score > 0.3:
            label = "positive"
        elif score < -0.3:
            label = "negative"
        else:
            label = "neutral"

    return {
        "score": round(score, 3),
        "label": label,
        "positive_count": positive_count,
        "negative_count": negative_count
    }

def summarize_text_fallback(text: str, max_sentences: int = 3) -> str:
    """
    Fallback text summarizer using simple extractive summarization.
    Extracts most important sentences based on keyword density.
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if len(sentences) <= max_sentences:
        return '. '.join(sentences) + '.'

    # Score sentences based on keyword presence
    scored_sentences = []
    for sentence in sentences:
        score = 0
        sentence_lower = sentence.lower()

        # Prioritize sentences with economic/forex keywords
        important_keywords = POSITIVE_KEYWORDS + NEGATIVE_KEYWORDS + [
            "central bank", "fed", "ecb", "interest rate", "inflation",
            "gdp", "employment", "forex", "currency", "dollar", "euro"
        ]

        for keyword in important_keywords:
            if keyword in sentence_lower:
                score += 1

        scored_sentences.append((sentence, score))

    # Sort by score and take top sentences
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    top_sentences = [s[0] for s in scored_sentences[:max_sentences]]

    return '. '.join(top_sentences) + '.'

def analyze_news_sentiment(articles: List[Dict]) -> Dict:
    """
    Analyze sentiment across multiple news articles.
    Returns aggregated sentiment and top insights.
    """
    if not articles:
        return {
            "overall_sentiment": "neutral",
            "sentiment_score": 0,
            "total_articles": 0,
            "sentiment_breakdown": {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            }
        }

    sentiments = []
    breakdown = {"positive": 0, "neutral": 0, "negative": 0}

    for article in articles:
        text = f"{article.get('title', '')} {article.get('summary', '')}"
        sentiment = analyze_sentiment_fallback(text)
        sentiments.append(sentiment['score'])
        breakdown[sentiment['label']] += 1

    avg_score = sum(sentiments) / len(sentiments)

    if avg_score > 0.2:
        overall = "positive"
    elif avg_score < -0.2:
        overall = "negative"
    else:
        overall = "neutral"

    return {
        "overall_sentiment": overall,
        "sentiment_score": round(avg_score, 3),
        "total_articles": len(articles),
        "sentiment_breakdown": breakdown
    }

def generate_news_summary(articles: List[Dict], max_items: int = 5) -> List[Dict]:
    """
    Generate summarized news feed with sentiment scoring.
    """
    summarized = []

    for article in articles[:max_items]:
        title = article.get("title", "")
        content = article.get("content", article.get("summary", ""))

        # Analyze sentiment
        sentiment = analyze_sentiment_fallback(f"{title} {content}")

        # Generate summary
        summary = summarize_text_fallback(content, max_sentences=2)

        summarized.append({
            "title": title,
            "summary": summary,
            "sentiment": sentiment["label"],
            "sentiment_score": sentiment["score"],
            "source": article.get("source", "Unknown"),
            "timestamp": article.get("timestamp", datetime.utcnow().isoformat()),
            "url": article.get("url", "#")
        })

    return summarized
