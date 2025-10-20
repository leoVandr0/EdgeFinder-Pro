# EdgeFinder Pro - System Architecture

## Overview

EdgeFinder Pro is a cloud-native, microservices-based forex analytics platform built with modern web technologies and deployed on serverless/container infrastructure.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         End Users                                │
│                    (Web Browsers / Mobile)                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ HTTPS
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Netlify CDN (Global)                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           React SPA (Vite Build)                          │  │
│  │  - Dashboard    - Currency Strength   - Pair Compare     │  │
│  │  - Events       - Insights            - News             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ REST API (HTTPS)
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Railway Platform                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend (Docker)                     │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │              API Routers                         │     │  │
│  │  │  - /api/strength      - /api/insights           │     │  │
│  │  │  - /api/events        - /api/pair-compare       │     │  │
│  │  │  - /api/news-summary                            │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                         ↓                                 │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │           Business Logic Services                │     │  │
│  │  │  - analytics.py   (Currency strength calc)      │     │  │
│  │  │  - sentiment.py   (NLP & summarization)         │     │  │
│  │  │  - db.py          (Database connections)        │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                         ↓                                 │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │              Data Models                         │     │  │
│  │  │  - Event      - CurrencyStrength  - Insight     │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────┬───────────────────────────┬───────────────────────┘
              │                           │
              │                           │
              ↓                           ↓
┌─────────────────────────┐   ┌─────────────────────────┐
│  PostgreSQL (Railway)   │   │  MongoDB Atlas (Cloud)  │
│  ─────────────────────  │   │  ─────────────────────  │
│  - Currency strengths   │   │  - Economic events      │
│  - Trade insights       │   │  - News articles        │
│  - Historical data      │   │  - User watchlists      │
└─────────────────────────┘   └─────────────────────────┘
```

## Component Details

### Frontend Layer (Netlify)

**Technology Stack:**
- React 18.2 with functional components
- Vite 5.0 (build tool)
- Tailwind CSS (styling)
- Recharts (data visualization)
- Axios (HTTP client)
- React Router v6 (routing)

**Deployment:**
- Static site generation
- Global CDN distribution
- Automatic HTTPS
- SPA routing via `_redirects`

**Pages:**
1. **Dashboard** - Overview with top insights, strength rankings, upcoming events
2. **Strength** - Currency strength visualization and comparison
3. **Events** - Economic calendar with filtering
4. **Compare** - Side-by-side pair analysis
5. **Insights** - AI-generated trade signals
6. **News** - Sentiment-analyzed market news

### Backend Layer (Railway)

**Technology Stack:**
- FastAPI 0.109 (async framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- SQLAlchemy (ORM)
- Motor (async MongoDB driver)

**API Design:**
- RESTful architecture
- OpenAPI 3.0 specification
- Auto-generated documentation (/docs)
- CORS middleware
- Request validation
- Error handling

**Endpoints:**
```
GET  /                          - Health check & API info
GET  /health                    - Health check
GET  /api/strength/             - All currency strengths
GET  /api/insights/             - Trade signals
GET  /api/events/               - Economic calendar
GET  /api/pair-compare/         - Pair comparison
GET  /api/news-summary/         - News with sentiment
```

### Data Layer

#### PostgreSQL (Railway)
**Schema:**
```sql
CREATE TABLE strengths (
    id SERIAL PRIMARY KEY,
    currency VARCHAR(3) UNIQUE,
    strength_score FLOAT,
    momentum FLOAT,
    trend VARCHAR(10),
    rank INTEGER,
    updated_at TIMESTAMP
);

CREATE TABLE insights (
    id SERIAL PRIMARY KEY,
    pair VARCHAR(10),
    signal_type VARCHAR(10),
    confidence FLOAT,
    entry_price FLOAT,
    stop_loss FLOAT,
    take_profit FLOAT,
    reasoning TEXT,
    timeframe VARCHAR(5),
    created_at TIMESTAMP
);
```

#### MongoDB Atlas
**Collections:**
```javascript
// events collection
{
    _id: ObjectId,
    currency: String,
    event_name: String,
    impact: String,
    actual: String,
    forecast: String,
    previous: String,
    timestamp: Date
}

// news collection (future)
{
    _id: ObjectId,
    title: String,
    content: String,
    source: String,
    sentiment: String,
    sentiment_score: Number,
    timestamp: Date
}
```

## Data Flow

### Currency Strength Calculation Flow

```
User Request
    ↓
Frontend (Strength.jsx)
    ↓
API Client (axios)
    ↓
GET /api/strength/
    ↓
strength.py Router
    ↓
analytics.py Service
    ↓
calculate_currency_strength()
    ├─ Fetch base scores
    ├─ Apply momentum calculation
    ├─ Determine trend (bullish/bearish/neutral)
    ├─ Rank currencies
    └─ Return StrengthResponse
    ↓
JSON Response
    ↓
Frontend Rendering (Recharts)
```

### Trading Insight Generation Flow

```
User Request
    ↓
GET /api/insights/?limit=10
    ↓
insights.py Router
    ↓
analytics.py Service
    ↓
generate_trade_insights()
    ├─ Get currency strengths
    ├─ Calculate divergences for all pairs
    ├─ Filter high-confidence signals
    ├─ Calculate entry/stop/target levels
    ├─ Generate reasoning text
    └─ Sort by confidence
    ↓
PostgreSQL (optional caching)
    ↓
JSON Response (List[Insight])
```

## Security Architecture

### Authentication Flow (Future)
```
User Login
    ↓
POST /auth/login
    ↓
Validate credentials
    ↓
Generate JWT token
    ↓
Return token + refresh token
    ↓
Client stores in localStorage
    ↓
Include in Authorization header
    ↓
Middleware validates JWT
    ↓
Allow/Deny request
```

### Current Security Measures

1. **Transport Security**
   - HTTPS enforced (Netlify + Railway)
   - TLS 1.3

2. **CORS Protection**
   - Whitelist origin validation
   - Credential support

3. **Input Validation**
   - Pydantic models
   - Type checking
   - Range validation

4. **Environment Isolation**
   - Secrets in env variables
   - No credentials in code
   - .gitignore for sensitive files

## Scalability Considerations

### Current Capacity
- **Frontend:** Unlimited (CDN)
- **Backend:** ~500 req/min (single Railway container)
- **Database:**
  - PostgreSQL: 100 concurrent connections
  - MongoDB: 500 concurrent connections

### Scaling Strategy

#### Horizontal Scaling
```
Load Balancer (Railway)
    ├─ Backend Instance 1
    ├─ Backend Instance 2
    └─ Backend Instance N
         ↓
    Connection Pool
         ↓
    Database Cluster
```

#### Caching Layer (Future)
```
Client Request
    ↓
Check Redis Cache
    ├─ Hit → Return cached data
    └─ Miss ↓
        Compute/Fetch from DB
            ↓
        Store in Redis (TTL: 5min)
            ↓
        Return to client
```

### Performance Optimization

1. **Frontend**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Memoization

2. **Backend**
   - Database connection pooling
   - Async I/O
   - Query optimization
   - Response caching

3. **Database**
   - Indexes on frequently queried fields
   - Query result caching
   - Read replicas (future)

## Monitoring & Observability

### Metrics to Track

1. **Application Metrics**
   - Request rate
   - Response time (p50, p95, p99)
   - Error rate
   - Active users

2. **Infrastructure Metrics**
   - CPU usage
   - Memory usage
   - Network I/O
   - Database connections

3. **Business Metrics**
   - Daily active users
   - API calls per user
   - Feature usage
   - Conversion rate

### Logging Strategy

```
Application → Structured Logs → Railway/Netlify
                                      ↓
                              Log Aggregation
                                      ↓
                              Analysis & Alerts
```

## CI/CD Pipeline

```
Developer Push to GitHub
    ↓
GitHub Actions Trigger
    ↓
┌──────────────────┬──────────────────┐
│  Backend Pipeline │ Frontend Pipeline │
│  ───────────────  │  ───────────────  │
│  1. Checkout code │  1. Checkout code │
│  2. Run tests     │  2. Install deps  │
│  3. Build Docker  │  3. Build static  │
│  4. Railway CLI   │  4. Netlify CLI   │
│  5. Deploy        │  5. Deploy        │
└──────────────────┴──────────────────┘
    ↓                       ↓
Railway Platform      Netlify CDN
```

## Disaster Recovery

### Backup Strategy

1. **Database Backups**
   - PostgreSQL: Daily automated backups (Railway)
   - MongoDB: Point-in-time recovery (Atlas)

2. **Code Backups**
   - GitHub repository (primary)
   - Local clones (secondary)

3. **Configuration Backups**
   - Environment variables documented
   - Infrastructure as Code (railway.json, netlify.toml)

### Recovery Procedures

**Backend Failure:**
1. Check Railway logs
2. Rollback to previous deployment
3. Verify health endpoint
4. Monitor for 30 minutes

**Frontend Failure:**
1. Check Netlify build logs
2. Rollback to previous deployment
3. Clear CDN cache
4. Test all pages

**Database Failure:**
1. Contact support (Railway/Atlas)
2. Restore from latest backup
3. Run data integrity checks
4. Resume services

## Future Enhancements

### Phase 2: Authentication & User Management
- JWT-based authentication
- User registration/login
- Password reset flow
- OAuth integration (Google, GitHub)

### Phase 3: Real-time Features
- WebSocket connections
- Live price updates
- Push notifications
- Alert system

### Phase 4: Advanced Analytics
- Machine learning models
- Backtesting engine
- Portfolio tracking
- Historical chart analysis

### Phase 5: Enterprise Features
- Multi-tenancy
- Role-based access control
- API rate limiting per user
- Custom webhooks
- White-label options

---

**Architecture Version:** 1.0
**Last Updated:** 2025-10-20
**Maintained By:** EdgeFinder Pro Team
