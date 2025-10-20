# EdgeFinder Pro - Deployment Checklist

## Pre-Deployment Checklist

### 1. Code Repository
- [ ] Create GitHub repository
- [ ] Push all code to `main` branch
- [ ] Verify `.gitignore` excludes sensitive files
- [ ] Review and update README.md

### 2. Environment Setup
- [ ] Railway account created
- [ ] Netlify account created
- [ ] MongoDB Atlas account created (optional)

## Backend Deployment (Railway)

### Step 1: Database Setup

#### PostgreSQL (Railway)
1. Go to Railway dashboard
2. Create new project
3. Click "+ New" → "Database" → "PostgreSQL"
4. Note the connection URL (auto-populated in `DATABASE_URL`)

#### MongoDB Atlas (Optional)
1. Go to [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
2. Create free cluster
3. Database Access → Add User (username/password)
4. Network Access → Add IP `0.0.0.0/0`
5. Copy connection string

### Step 2: Deploy Backend

1. **In Railway Dashboard:**
   - Click "+ New" → "GitHub Repo"
   - Select `edgefinder-pro` repository
   - Choose `backend` as root directory

2. **Configure Environment Variables:**
   ```
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/edgefinder
   ALLOWED_ORIGINS=https://your-site.netlify.app,http://localhost:5173
   ENVIRONMENT=production
   PORT=8000
   OPENAI_API_KEY=sk-... (optional)
   ```

3. **Generate Domain:**
   - Settings → Generate Domain
   - Note the URL (e.g., `https://edgefinder-backend.railway.app`)

4. **Verify Deployment:**
   ```bash
   curl https://your-backend.railway.app/health
   curl https://your-backend.railway.app/docs
   ```

### Step 3: Seed Database (Optional)

```bash
# SSH into Railway or run locally with production DB
railway run python backend/seed_data/load_data.py
```

## Frontend Deployment (Netlify)

### Step 1: Deploy to Netlify

1. **In Netlify Dashboard:**
   - Sites → Add new site → Import existing project
   - Connect to GitHub
   - Select `edgefinder-pro` repository

2. **Build Settings:**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```

3. **Environment Variables:**
   - Site settings → Environment variables
   - Add:
     ```
     VITE_API_BASE_URL=https://your-backend.railway.app
     ```

4. **Deploy Site:**
   - Click "Deploy site"
   - Wait for build to complete

5. **Custom Domain (Optional):**
   - Domain settings → Add custom domain
   - Follow DNS configuration steps

### Step 2: Update Backend CORS

1. Go back to Railway
2. Update `ALLOWED_ORIGINS` environment variable:
   ```
   ALLOWED_ORIGINS=https://your-site.netlify.app
   ```
3. Redeploy backend

### Step 3: Test Frontend

1. Visit your Netlify URL
2. Verify all pages load:
   - [ ] Dashboard
   - [ ] Strength
   - [ ] Events
   - [ ] Compare
   - [ ] Insights
   - [ ] News
3. Check browser console for errors
4. Test API calls (Network tab)

## CI/CD Setup (GitHub Actions)

### Step 1: Get API Tokens

**Railway:**
1. Railway → Account Settings → Tokens
2. Create new token
3. Copy token

**Netlify:**
1. User Settings → Applications → Personal access tokens
2. Create new token
3. Copy token
4. Site Settings → General → Site details
5. Copy Site ID

### Step 2: Add GitHub Secrets

1. Repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `RAILWAY_TOKEN`
   - `RAILWAY_API_URL` (your backend URL)
   - `NETLIFY_AUTH_TOKEN`
   - `NETLIFY_SITE_ID`
   - `VITE_API_BASE_URL` (your backend URL)

### Step 3: Test Workflows

1. Make a small change to backend code
2. Push to `main` branch
3. Check Actions tab for deployment status
4. Verify backend updated

5. Make a small change to frontend code
6. Push to `main` branch
7. Check Actions tab
8. Verify frontend updated

## Post-Deployment

### Monitoring Setup

1. **Railway Logs:**
   ```bash
   railway logs
   ```

2. **Netlify Logs:**
   - Deploys → Deploy log

3. **Error Tracking (Optional):**
   - Set up Sentry
   - Add DSN to environment variables

### Performance Testing

1. **Backend Performance:**
   ```bash
   # Test API response time
   curl -w "@curl-format.txt" -o /dev/null -s https://your-backend.railway.app/api/strength/
   ```

2. **Frontend Performance:**
   - Run Lighthouse audit in Chrome DevTools
   - Target scores: Performance > 90, Accessibility > 95

### Security Checklist

- [ ] HTTPS enabled (automatic on Railway/Netlify)
- [ ] CORS configured correctly
- [ ] Environment variables secured
- [ ] No secrets in code
- [ ] Database credentials secured
- [ ] API rate limiting configured (optional)

## Troubleshooting

### Backend Issues

**Problem:** 502 Bad Gateway
- Check Railway logs: `railway logs`
- Verify environment variables
- Check database connections

**Problem:** CORS errors
- Verify `ALLOWED_ORIGINS` includes Netlify URL
- Check for trailing slashes
- Redeploy backend after changes

### Frontend Issues

**Problem:** Blank page
- Check browser console
- Verify API URL in environment
- Check Netlify build logs

**Problem:** API calls fail
- Verify backend is running
- Check CORS configuration
- Verify API URL format (no trailing slash)

## Rollback Procedure

### Backend Rollback
1. Railway → Deployments
2. Find previous successful deployment
3. Click "Redeploy"

### Frontend Rollback
1. Netlify → Deploys
2. Find previous deployment
3. Click "Publish deploy"

## Cost Estimation

### Free Tier Limits

**Railway:**
- $5 free credit/month
- ~500 hours of runtime
- Sufficient for testing

**Netlify:**
- 100GB bandwidth/month
- 300 build minutes/month
- Free for personal projects

**MongoDB Atlas:**
- 512MB storage free
- Sufficient for development

### Paid Tiers (if needed)

**Railway:** $5-20/month
**Netlify Pro:** $19/month
**MongoDB Atlas:** $9/month (M2 cluster)

## Maintenance

### Weekly Tasks
- [ ] Check error logs
- [ ] Monitor API response times
- [ ] Review usage metrics

### Monthly Tasks
- [ ] Update dependencies
- [ ] Review and optimize database queries
- [ ] Check for security updates
- [ ] Backup database

### Quarterly Tasks
- [ ] Performance audit
- [ ] Security audit
- [ ] Cost optimization review
- [ ] User feedback review

## Support Resources

- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Netlify Docs:** [docs.netlify.com](https://docs.netlify.com)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Docs:** [react.dev](https://react.dev)

---

**Deployment Date:** _____________

**Deployed By:** _____________

**Backend URL:** _____________

**Frontend URL:** _____________
