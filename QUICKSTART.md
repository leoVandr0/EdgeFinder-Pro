# EdgeFinder Pro - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Local Development

#### 1. Backend (Terminal 1)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000
📚 API Docs at: http://localhost:8000/docs

#### 2. Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Run dev server
npm run dev
```

✅ Frontend running at: http://localhost:5173

---

## ☁️ Deploy to Production

### Backend → Railway (2 minutes)

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select `edgefinder-pro/backend`
4. Add environment variables:
   ```
   ALLOWED_ORIGINS=https://your-site.netlify.app
   ENVIRONMENT=production
   ```
5. Generate domain → Copy URL

### Frontend → Netlify (2 minutes)

1. Go to [app.netlify.com](https://app.netlify.com)
2. New site from Git → Select repo
3. Build settings:
   - Base: `frontend`
   - Build: `npm run build`
   - Publish: `frontend/dist`
4. Environment variables:
   ```
   VITE_API_BASE_URL=https://your-backend.railway.app
   ```
5. Deploy site

---

## 🧪 Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get currency strengths
curl http://localhost:8000/api/strength/

# Get trading insights
curl http://localhost:8000/api/insights/

# Get economic events
curl http://localhost:8000/api/events/

# Compare EUR/USD
curl http://localhost:8000/api/pair-compare?base=EUR&quote=USD

# Get news summaries
curl http://localhost:8000/api/news-summary/
```

---

## 📁 Project Structure

```
edgefinder-pro/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── routers/     # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── models/      # Data models
│   │   └── main.py      # App entry point
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/      # Dashboard, Strength, etc.
│   │   ├── components/ # Reusable UI components
│   │   └── api/        # API client
│   ├── netlify.toml
│   └── package.json
│
└── .github/workflows/  # CI/CD pipelines
```

---

## 🔑 Key Features

### Currency Strength Analysis
Real-time strength scores for 8 major currencies (USD, EUR, GBP, JPY, CHF, AUD, CAD, NZD)

### Pair Comparison
Side-by-side analysis with divergence calculations and trading recommendations

### Economic Calendar
High-impact event tracking with forecast vs actual data

### Trading Insights
AI-generated trade signals with confidence scoring and entry/exit levels

### News Sentiment
Summarized forex news with sentiment analysis (positive/negative/neutral)

---

## 🛠️ Common Tasks

### Add a New API Endpoint

1. Create router in `backend/app/routers/`
2. Register in `backend/app/main.py`
3. Create frontend API method in `frontend/src/api/api.js`
4. Add page/component in `frontend/src/pages/`

### Update Environment Variables

**Backend (Railway):**
Dashboard → Variables → Add/Edit

**Frontend (Netlify):**
Site settings → Environment variables → Add/Edit

### View Logs

```bash
# Railway
railway logs

# Netlify
netlify logs
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.11+)
- Verify dependencies: `pip list`
- Check logs for errors

### Frontend can't connect to API
- Verify `VITE_API_BASE_URL` in `.env`
- Check backend is running: `curl http://localhost:8000/health`
- Check browser console for CORS errors

### Database errors
- PostgreSQL: Check `POSTGRES_URL` environment variable
- MongoDB: Check `MONGODB_URI` environment variable
- Both are optional - app runs with in-memory fallback

---

## 📚 Next Steps

1. ✅ Complete local development setup
2. ✅ Deploy backend to Railway
3. ✅ Deploy frontend to Netlify
4. ✅ Set up CI/CD with GitHub Actions
5. 🎯 Add authentication (JWT)
6. 🎯 Implement user watchlists
7. 🎯 Add email notifications
8. 🎯 Create mobile app

---

## 🆘 Get Help

- **Documentation:** See [README.md](README.md)
- **Deployment Guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **API Docs:** http://localhost:8000/docs (when running)
- **Issues:** Create issue on GitHub

---

**Built with FastAPI, React, Railway, and Netlify**
