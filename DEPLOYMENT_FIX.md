# Deployment Configuration Fix for Richy's Board

## Problem Diagnosis

The dashboard is showing "Failed to load dashboard data" because the **frontend deployed on Netlify doesn't know where to find the backend API on Railway**.

### Root Cause
When Vite builds your frontend for production, it looks for the `VITE_API_BASE_URL` environment variable. If it's not set, it defaults to `http://localhost:8000`, which doesn't exist in production.

## Solution: 3-Step Configuration Fix

### Step 1: Find Your Railway Backend URL

1. Go to [railway.app](https://railway.app) and log in
2. Open your Richy's Board backend project
3. Click on "Settings" tab
4. Under "Domains", you'll see your backend URL
   - It looks like: `https://your-project-name.up.railway.app`
   - **Copy this URL** (we'll use it in the next steps)

### Step 2: Configure Netlify Environment Variable

You need to tell Netlify where your backend is hosted:

#### Option A: Netlify Dashboard (Recommended)

1. Go to [app.netlify.com](https://app.netlify.com)
2. Select your Richy's Board site
3. Go to **Site settings** → **Environment variables**
4. Click **Add a variable**
5. Enter:
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://your-project-name.up.railway.app` (from Step 1)
6. Click **Save**
7. Go to **Deploys** tab and click **Trigger deploy** → **Clear cache and deploy site**

#### Option B: Netlify CLI

```bash
cd frontend

# Set the environment variable
netlify env:set VITE_API_BASE_URL "https://your-project-name.up.railway.app"

# Trigger a new deployment
netlify deploy --prod
```

### Step 3: Configure Railway CORS

Your Railway backend needs to allow requests from your Netlify frontend:

#### Option A: Railway Dashboard (Recommended)

1. Go to [railway.app](https://railway.app)
2. Open your backend project
3. Go to **Variables** tab
4. Find or add `ALLOWED_ORIGINS`
5. Set its value to:
   ```
   https://lustrous-pudding-fda54c.netlify.app,http://localhost:5173
   ```
   *(Replace with your actual Netlify URL if different)*
6. Click **Deploy** to restart the backend with new config

#### Option B: Railway CLI

```bash
cd backend

# Set CORS origins
railway variables set ALLOWED_ORIGINS="https://lustrous-pudding-fda54c.netlify.app,http://localhost:5173"

# Deploy
railway up
```

## Verification Steps

After completing all 3 steps, verify the fix:

### 1. Check Backend is Running

Open your browser and go to:
```
https://your-project-name.up.railway.app/health
```

You should see:
```json
{"status": "healthy"}
```

### 2. Check Frontend Build

Go to Netlify → Deploys → Latest deploy → Deploy log

Search for `VITE_API_BASE_URL` in the log. You should see:
```
Environment variable VITE_API_BASE_URL detected
```

### 3. Test the Dashboard

1. Open your Netlify site: `https://lustrous-pudding-fda54c.netlify.app`
2. Open browser DevTools (F12)
3. Go to **Console** tab
4. Refresh the page
5. You should see API requests like:
   ```
   API Request: GET /api/strength/
   API Request: GET /api/insights/?limit=5
   API Request: GET /api/events/high-impact
   ```
6. Check the **Network** tab
7. Click on any API request (e.g., `strength`)
8. Verify:
   - **Request URL** should be `https://your-backend.railway.app/api/strength/`
   - **Status** should be `200 OK`
   - **Response** should contain data

### 4. Test Service Worker

In DevTools **Console**, check for:
```
Service Worker registered successfully
```

No icon errors should appear.

## Troubleshooting

### Issue: Still seeing localhost:8000 in Network tab

**Cause:** Netlify didn't rebuild with the environment variable

**Fix:**
1. Verify variable is set: Netlify Dashboard → Site settings → Environment variables
2. Clear cache and redeploy: Deploys → Trigger deploy → **Clear cache and deploy site**

### Issue: CORS error in console

**Example error:**
```
Access to fetch at 'https://backend.railway.app/api/strength/' from origin 'https://your-site.netlify.app'
has been blocked by CORS policy
```

**Cause:** Railway backend doesn't allow your Netlify domain

**Fix:**
1. Verify Railway `ALLOWED_ORIGINS` includes your Netlify URL
2. Make sure there are NO spaces after commas in the origins list
3. Restart the Railway backend

### Issue: Service Worker caching old/broken responses

**Cause:** Service worker is serving stale cached data

**Fix:**
1. Open DevTools → **Application** tab
2. Go to **Service Workers** section
3. Click **Unregister** next to your service worker
4. Go to **Storage** section
5. Click **Clear site data**
6. Refresh the page (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: Backend is not deployed

**Check Railway logs:**
```bash
railway logs
```

Look for errors like:
- Missing dependencies
- Port binding issues
- Database connection errors

## Quick Reference

### Your Current URLs

| Service | URL |
|---------|-----|
| Frontend (Netlify) | `https://lustrous-pudding-fda54c.netlify.app` |
| Backend (Railway) | `https://????.up.railway.app` ← **You need to find this** |

### Environment Variables Checklist

#### Netlify (Frontend)
- [ ] `VITE_API_BASE_URL` = Railway backend URL

#### Railway (Backend)
- [ ] `ALLOWED_ORIGINS` = Netlify frontend URL + localhost
- [ ] `PORT` = 8000 (should be set automatically)
- [ ] `ENVIRONMENT` = production (optional)
- [ ] `MONGODB_URI` = Your MongoDB connection string (optional)
- [ ] `POSTGRES_URL` = Your PostgreSQL URL (optional)

## Next Steps After Fix

Once the dashboard loads correctly:

1. **Test PWA Installation**
   - On mobile or desktop Chrome
   - You should see an install prompt
   - Icons should load correctly

2. **Test Offline Mode**
   - Open DevTools → Network tab
   - Check "Offline" checkbox
   - Refresh page
   - Should show "You're offline. Showing cached data." banner
   - Last loaded data should still display

3. **Monitor for Errors**
   - Check Railway logs: `railway logs --tail`
   - Check Netlify deploy logs
   - Monitor browser console for any API errors

## Files Modified

The following files have been updated to support proper deployment:

1. `frontend/netlify.toml` - Added PWA headers and environment variable documentation
2. `frontend/public/manifest.json` - PWA configuration
3. `frontend/public/sw.js` - Service worker for offline support
4. `frontend/src/components/PWAInstallPrompt.jsx` - Install prompt component
5. `frontend/src/components/OfflineIndicator.jsx` - Offline detection

## Support

If you're still experiencing issues after following this guide:

1. Check the browser console for specific error messages
2. Check Railway logs for backend errors
3. Verify all environment variables are set correctly
4. Try clearing browser cache and service worker
5. Test the backend API directly using curl or Postman

---

**Last Updated:** 2025-10-21
**Status:** Configuration incomplete - awaiting Railway backend URL
