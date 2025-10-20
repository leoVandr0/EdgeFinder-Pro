# EdgeFinder Pro API Reference

## Base URL

**Production:** `https://your-backend.railway.app`
**Development:** `http://localhost:8000`

## Authentication

Currently no authentication required. Future versions will implement JWT-based authentication.

## Rate Limiting

No rate limiting currently implemented. Future versions will enforce:
- 100 requests per minute (free tier)
- 1000 requests per minute (premium tier)

---

## Endpoints

### Health & Info

#### GET /
Returns API information and available endpoints.

**Response:**
```json
{
  "service": "EdgeFinder Pro API",
  "status": "operational",
  "version": "1.0.0",
  "endpoints": {
    "docs": "/docs",
    "strength": "/api/strength",
    "insights": "/api/insights",
    "events": "/api/events",
    "pair_compare": "/api/pair-compare",
    "news_summary": "/api/news-summary"
  }
}
```

#### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Currency Strength

### GET /api/strength/

Get strength scores for all major currencies.

**Parameters:** None

**Response:**
```json
{
  "strengths": {
    "USD": {
      "currency": "USD",
      "strength_score": 75.5,
      "momentum": 2.3,
      "trend": "bullish",
      "rank": 1
    },
    "EUR": {
      "currency": "EUR",
      "strength_score": 68.2,
      "momentum": -1.2,
      "trend": "bearish",
      "rank": 3
    }
    // ... other currencies
  },
  "updated_at": "2025-10-20T14:30:00.000Z"
}
```

**Example:**
```bash
curl https://your-backend.railway.app/api/strength/
```

### GET /api/strength/currency/{currency_code}

Get strength data for a specific currency.

**Path Parameters:**
- `currency_code` (string, required): 3-letter currency code (USD, EUR, etc.)

**Response:**
```json
{
  "currency": "USD",
  "data": {
    "currency": "USD",
    "strength_score": 75.5,
    "momentum": 2.3,
    "trend": "bullish",
    "rank": 1
  },
  "updated_at": "2025-10-20T14:30:00.000Z"
}
```

**Example:**
```bash
curl https://your-backend.railway.app/api/strength/currency/USD
```

**Error Responses:**
- `404`: Currency not found
- `500`: Internal server error

---

## Trading Insights

### GET /api/insights/

Get AI-generated trading insights and signals.

**Query Parameters:**
- `limit` (integer, optional): Number of insights to return (1-50, default: 10)

**Response:**
```json
[
  {
    "pair": "EUR/USD",
    "signal_type": "buy",
    "confidence": 82.5,
    "entry_price": 1.0950,
    "stop_loss": 1.0900,
    "take_profit": 1.1050,
    "reasoning": "Strong USD weakness combined with positive EU data",
    "timeframe": "H4"
  },
  {
    "pair": "GBP/USD",
    "signal_type": "sell",
    "confidence": 76.3,
    "entry_price": 1.2650,
    "stop_loss": 1.2700,
    "take_profit": 1.2550,
    "reasoning": "GBP showing weakness against strong USD momentum",
    "timeframe": "H4"
  }
  // ... more insights
]
```

**Example:**
```bash
curl https://your-backend.railway.app/api/insights/?limit=5
```

### GET /api/insights/pair/{pair}

Get insights for a specific currency pair.

**Path Parameters:**
- `pair` (string, required): Currency pair (EUR/USD, EURUSD, EUR-USD)

**Response:**
```json
[
  {
    "pair": "EUR/USD",
    "signal_type": "buy",
    "confidence": 82.5,
    "entry_price": 1.0950,
    "stop_loss": 1.0900,
    "take_profit": 1.1050,
    "reasoning": "Strong USD weakness combined with positive EU data",
    "timeframe": "H4"
  }
]
```

**Example:**
```bash
curl https://your-backend.railway.app/api/insights/pair/EUR/USD
curl https://your-backend.railway.app/api/insights/pair/EURUSD
```

**Error Responses:**
- `400`: Invalid pair format
- `404`: No insights found for pair

---

## Economic Events

### GET /api/events/

Get economic calendar events.

**Query Parameters:**
- `currency` (string, optional): Filter by currency code (USD, EUR, etc.)
- `impact` (string, optional): Filter by impact level (High, Medium, Low)
- `upcoming` (boolean, optional): Show only upcoming events (default: true)

**Response:**
```json
[
  {
    "currency": "USD",
    "event_name": "Non-Farm Payrolls",
    "impact": "High",
    "actual": "250K",
    "forecast": "200K",
    "previous": "180K",
    "timestamp": "2025-10-22T14:30:00.000Z"
  },
  {
    "currency": "EUR",
    "event_name": "ECB Interest Rate Decision",
    "impact": "High",
    "actual": null,
    "forecast": "4.50%",
    "previous": "4.25%",
    "timestamp": "2025-10-25T13:45:00.000Z"
  }
  // ... more events
]
```

**Examples:**
```bash
# All upcoming events
curl https://your-backend.railway.app/api/events/

# USD events only
curl https://your-backend.railway.app/api/events/?currency=USD

# High impact events only
curl https://your-backend.railway.app/api/events/?impact=High

# Past events
curl https://your-backend.railway.app/api/events/?upcoming=false
```

### GET /api/events/today

Get all economic events scheduled for today.

**Parameters:** None

**Response:** Same format as `/api/events/`

**Example:**
```bash
curl https://your-backend.railway.app/api/events/today
```

### GET /api/events/high-impact

Get only high-impact economic events.

**Parameters:** None

**Response:** Same format as `/api/events/`

**Example:**
```bash
curl https://your-backend.railway.app/api/events/high-impact
```

---

## Pair Comparison

### GET /api/pair-compare/

Compare two currencies in a pair.

**Query Parameters:**
- `base` (string, required): Base currency code (e.g., EUR)
- `quote` (string, required): Quote currency code (e.g., USD)

**Response:**
```json
{
  "pair": "EUR/USD",
  "base_currency": {
    "currency": "EUR",
    "strength": 68.2,
    "momentum": -1.2,
    "trend": "bearish",
    "rank": 3
  },
  "quote_currency": {
    "currency": "USD",
    "strength": 75.5,
    "momentum": 2.3,
    "trend": "bullish",
    "rank": 1
  },
  "divergence": -7.3,
  "recommendation": "Sell",
  "confidence": 78.5,
  "analysis": "EUR is weaker than USD by 7.3 points."
}
```

**Example:**
```bash
curl "https://your-backend.railway.app/api/pair-compare/?base=EUR&quote=USD"
```

### GET /api/pair-compare/{pair}

Compare currency pair using direct notation.

**Path Parameters:**
- `pair` (string, required): Currency pair (EUR/USD, EURUSD, EUR-USD)

**Response:** Same format as `/api/pair-compare/`

**Examples:**
```bash
curl https://your-backend.railway.app/api/pair-compare/EUR/USD
curl https://your-backend.railway.app/api/pair-compare/EURUSD
curl https://your-backend.railway.app/api/pair-compare/EUR-USD
```

**Error Responses:**
- `400`: Invalid pair format or currency codes
- `404`: Currency pair not found

---

## News & Sentiment

### GET /api/news-summary/

Get AI-summarized forex news with sentiment analysis.

**Query Parameters:**
- `limit` (integer, optional): Number of articles to return (1-50, default: 10)
- `currency` (string, optional): Filter by currency mention

**Response:**
```json
{
  "total": 10,
  "articles": [
    {
      "title": "Federal Reserve Signals Potential Rate Cut in Q4",
      "summary": "The Federal Reserve indicated in today's meeting that interest rates may be reduced in the fourth quarter. Chair Powell emphasized data-dependent decision making.",
      "sentiment": "positive",
      "sentiment_score": 0.45,
      "source": "Reuters",
      "timestamp": "2025-10-20T12:30:00.000Z",
      "url": "https://example.com/fed-rate-cut"
    }
    // ... more articles
  ]
}
```

**Examples:**
```bash
# Get 5 latest articles
curl https://your-backend.railway.app/api/news-summary/?limit=5

# Get USD-related news
curl https://your-backend.railway.app/api/news-summary/?currency=USD
```

### GET /api/news-summary/sentiment

Get aggregated market sentiment from recent news.

**Parameters:** None

**Response:**
```json
{
  "overall_sentiment": "positive",
  "sentiment_score": 0.15,
  "total_articles": 10,
  "sentiment_breakdown": {
    "positive": 6,
    "neutral": 2,
    "negative": 2
  }
}
```

**Example:**
```bash
curl https://your-backend.railway.app/api/news-summary/sentiment
```

### GET /api/news-summary/currency/{currency_code}

Get news articles specifically mentioning a currency.

**Path Parameters:**
- `currency_code` (string, required): 3-letter currency code

**Query Parameters:**
- `limit` (integer, optional): Number of articles (1-20, default: 5)

**Response:**
```json
{
  "currency": "USD",
  "total": 5,
  "articles": [
    {
      "title": "US Dollar Strengthens on Strong Employment Report",
      "summary": "The US dollar rallied across the board following robust non-farm payrolls data...",
      "sentiment": "positive",
      "sentiment_score": 0.65,
      "source": "CNBC",
      "timestamp": "2025-10-20T10:00:00.000Z",
      "url": "https://example.com/usd-employment"
    }
    // ... more articles
  ],
  "sentiment": {
    "overall_sentiment": "positive",
    "sentiment_score": 0.42,
    "total_articles": 5,
    "sentiment_breakdown": {
      "positive": 4,
      "neutral": 1,
      "negative": 0
    }
  }
}
```

**Example:**
```bash
curl https://your-backend.railway.app/api/news-summary/currency/USD?limit=10
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid parameter value"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "An error occurred"
}
```

---

## Data Models

### CurrencyStrength
```typescript
{
  currency: string;        // 3-letter code
  strength_score: number;  // 0-100
  momentum: number;        // -10 to +10
  trend: string;          // "bullish" | "bearish" | "neutral"
  rank: number;           // 1-8
}
```

### Insight
```typescript
{
  pair: string;           // e.g., "EUR/USD"
  signal_type: string;    // "buy" | "sell" | "hold"
  confidence: number;     // 0-100
  entry_price: number;    // Suggested entry
  stop_loss: number;      // Stop loss level
  take_profit: number;    // Take profit target
  reasoning: string;      // AI-generated explanation
  timeframe: string;      // "H1" | "H4" | "D1"
}
```

### Event
```typescript
{
  currency: string;       // 3-letter code
  event_name: string;     // Event title
  impact: string;         // "High" | "Medium" | "Low"
  actual: string | null;  // Actual value
  forecast: string | null; // Forecast value
  previous: string | null; // Previous value
  timestamp: string;      // ISO 8601 datetime
}
```

---

## WebSocket API (Future)

Real-time updates will be available via WebSocket in future versions:

```javascript
const ws = new WebSocket('wss://your-backend.railway.app/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
};

// Subscribe to specific channels
ws.send(JSON.stringify({
  action: 'subscribe',
  channels: ['strength', 'insights', 'news']
}));
```

---

## SDK Examples

### JavaScript/TypeScript

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://your-backend.railway.app',
  timeout: 10000
});

// Get currency strengths
const strengths = await api.get('/api/strength/');

// Get trading insights
const insights = await api.get('/api/insights/', {
  params: { limit: 5 }
});

// Compare pair
const comparison = await api.get('/api/pair-compare/', {
  params: { base: 'EUR', quote: 'USD' }
});
```

### Python

```python
import requests

BASE_URL = 'https://your-backend.railway.app'

# Get currency strengths
response = requests.get(f'{BASE_URL}/api/strength/')
strengths = response.json()

# Get trading insights
response = requests.get(f'{BASE_URL}/api/insights/', params={'limit': 5})
insights = response.json()

# Compare pair
response = requests.get(f'{BASE_URL}/api/pair-compare/',
                       params={'base': 'EUR', 'quote': 'USD'})
comparison = response.json()
```

---

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation:
- Try endpoints directly from browser
- View request/response schemas
- See example responses
- Download OpenAPI specification

**URL:** https://your-backend.railway.app/docs

---

**API Version:** 1.0.0
**Last Updated:** 2025-10-20
**Support:** api-support@edgefinderpro.com
