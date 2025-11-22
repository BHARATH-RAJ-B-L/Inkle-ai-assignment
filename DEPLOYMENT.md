# Deployment Guide for TripMind AI

This guide documents the deployment configuration for the TripMind AI multi-agent tourism system.

---

## 🌐 Current Deployment

The application is currently deployed and accessible at:

- **Frontend:** https://tripmindai.netlify.app
- **Backend API:** https://inkle-ai-assignment.onrender.com
- **API Documentation:** https://inkle-ai-assignment.onrender.com/docs
- **GitHub Repository:** https://github.com/BHARATH-RAJ-B-L/Inkle-ai-assignment

---

## 🏗️ Architecture

### Frontend (Netlify)
- **Platform:** Netlify
- **Source:** `frontend/` directory
- **Build:** Static HTML/CSS/JavaScript (no build step required)
- **Auto-Deploy:** Enabled (deploys on git push to main)

### Backend (Render)
- **Platform:** Render Web Service
- **Source:** `backend/` directory  
- **Runtime:** Python 3.13
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## ⚙️ Environment Variables (Production)

### Backend (Render)
```bash
HOST=0.0.0.0
DEBUG=False
FRONTEND_URL=https://tripmindai.netlify.app
NOMINATIM_USER_AGENT=tripmind-production
```

> **Note:** PORT is automatically set by Render ($PORT variable)

---

## 📋 Deployment Checklist

- [x] Backend deployed to Render
- [x] Frontend deployed to Netlify  
- [x] Environment variables configured
- [x] CORS enabled for frontend domain
- [x] API endpoints tested
- [x] Frontend connected to backend
- [x] Repository pushed to GitHub
- [x] Documentation updated

---

## 🧪 Testing Deployed Application

### Health Check
```bash
curl https://inkle-ai-assignment.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Multi-Agent Tourism System"
}
```

### API Documentation
Visit: https://inkle-ai-assignment.onrender.com/docs

###  Full Test
1. Visit: https://tripmindai.netlify.app
2. Search for "Bangalore" or any city
3. Verify weather and places data loads correctly

---

## 🔧 Redeployment Instructions

### Backend (Render)
Changes are automatically deployed when you push to GitHub:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically:
1. Detect the new commit
2. Pull the latest code
3. Run build command
4. Restart the service

### Frontend (Netlify)
Same as backend - automatic deployment on git push to main.

---

## 💡 Render Free Tier Limitations

**Sleep Behavior:**
- Backend sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Subsequent requests are instant

**Workaround (Optional):**
Use [UptimeRobot](https://uptimerobot.com) (free) to ping the backend every 5 minutes:
- URL to monitor: `https://inkle-ai-assignment.onrender.com/api/health`
- Interval: 5 minutes

---

## 🛠️ Troubleshooting

### Issue: "Failed to connect to server"
**Solution:** 
- Check backend is running: visit https://inkle-ai-assignment.onrender.com/api/health
- If backend is sleeping, wait ~30 seconds for it to wake up

### Issue: CORS errors in browser console
**Solution:**
- Verify `FRONTEND_URL` environment variable in Render matches Netlify URL exactly
- Redeploy backend after updating variables

### Issue: Changes not reflected after git push
**Solution:**
- Check deployment logs in Render/Netlify dashboards
- Verify git push was successful
- Clear browser cache

---

## 📊 Monitoring

### Backend Logs
View real-time logs in Render Dashboard:
1. Go to https://dashboard.render.com
2. Click on `inkle-ai-assignment` service
3. Click "Logs" tab

### Frontend Deployment Status
View deployment history in Netlify Dashboard:
1. Go to https://app.netlify.com
2. Click on `tripmindai` site
3. Click "Deploys" tab

---

## 🔐 Security Notes

- ✅ `.env` file is gitignored (secrets not in repository)
- ✅ Environment variables configured in platform dashboards
- ✅ CORS restricted to frontend domain only
- ✅ Rate limiting enabled (10 requests/60 seconds per IP)
- ✅ Input validation and XSS prevention implemented

---

## 📱 Access URLs

| Resource | URL |
|----------|-----|
| **Live Application** | https://tripmindai.netlify.app |
| **Backend API** | https://inkle-ai-assignment.onrender.com |
| **API Docs (Interactive)** | https://inkle-ai-assignment.onrender.com/docs |
| **Health Check** | https://inkle-ai-assignment.onrender.com/api/health |
| **GitHub Repository** | https://github.com/BHARATH-RAJ-B-L/Inkle-ai-assignment |

---

**Deployment Complete!** 🎉 The application is live and publicly accessible.
