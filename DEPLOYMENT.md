# Deployment Guide for TripMind AI

This guide covers deployment options for the Inkle AI assignment submission.

## 🌐 Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) ⭐ Recommended

#### Frontend Deployment (Vercel)
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Configure:
   - Build Command: (leave empty, static site)
   - Output Directory: `frontend`
   - Install Command: (none needed)
5. Deploy

#### Backend Deployment (Render)
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python main.py`
   - Environment Variables:
     ```
     FRONTEND_URL=https://your-frontend.vercel.app
     ```
5. Deploy

**Update Frontend**: Edit `frontend/script.js` line 6:
```javascript
const API_BASE_URL = 'https://your-backend.onrender.com';
```

---

### Option 2: Railway (Full Stack)

1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Configure:
   - Root Directory: `backend`
   - Start Command: `python main.py`
5. Add environment variables
6. Deploy backend and note the URL
7. Deploy frontend separately or use static hosting

---

### Option 3: Heroku (Full Stack)

Create `Procfile` in root:
```
web: cd backend && python main.py
```

Create `runtime.txt`:
```
python-3.11.0
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
```

---

### Option 4: GitHub Pages (Frontend) + PythonAnywhere (Backend)

#### Frontend (GitHub Pages)
1. Push to GitHub
2. Go to Settings → Pages
3. Select branch and `/frontend` folder
4. Save

#### Backend (PythonAnywhere)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload backend files
3. Configure WSGI file
4. Set environment variables
5. Reload web app

---

## 📋 Pre-Deployment Checklist

- [ ] Remove debug statements
- [ ] Update CORS to allow your frontend domain
- [ ] Test all API endpoints
- [ ] Update README with deployment URLs
- [ ] Add your contact info to SUBMISSION.md
- [ ] Ensure .env is in .gitignore

---

## 🔧 Environment Variables for Production

```bash
# Backend (.env)
HOST=0.0.0.0
PORT=8000
DEBUG=False
FRONTEND_URL=https://your-frontend-url.com
NOMINATIM_USER_AGENT=tripmind-ai-production
NOMINATIM_EMAIL=your-email@example.com
```

---

## 🧪 Testing Deployment

After deployment, test:
1. Health check: `curl https://your-backend.com/api/health`
2. API docs: Visit `https://your-backend.com/docs`
3. Full test: Search "Bangalore" on frontend

---

## 📤 GitHub Repository Setup

### 1. Initialize Git (if not done)
```bash
cd "c:\Users\Bharath Raj B L\Desktop\Inkle ai assignment"
git init
git add .
git commit -m "Initial commit: TripMind AI - Multi-Agent Tourism System"
```

### 2. Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. Name: `tripmind-ai-inkle-assignment`
3. Public repository
4. Don't initialize with README (we have one)

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/tripmind-ai-inkle-assignment.git
git branch -M main
git push -u origin main
```

### 4. Make Repository Public
- Go to Settings → Danger Zone → Change visibility → Make public

---

## 📝 Final Submission Steps

1. **Deploy Application**
   - Choose deployment option above
   - Test thoroughly

2. **Update SUBMISSION.md**
   - Add repository URL
   - Add deployed application URL
   - Add your contact info

3. **Create Public Links**
   - Ensure GitHub repo is public
   - Test deployment URLs work
   - Verify anyone can access

4. **Submit to Inkle**
   - Email submission with:
     - GitHub repository link
     - Deployed application link
     - SUBMISSION.md (or copy content to email)

---

## 🎯 Quick Deploy (5 minutes)

**Fastest option for submission:**

1. Push to GitHub (2 min)
2. Deploy backend to Render (2 min)
3. Update frontend API URL (30 sec)
4. Host frontend on Vercel (30 sec)
5. Test and submit! ✅

**Total time**: ~5 minutes
**Cost**: $0 (free tiers)

---

Good luck with your submission! 🎉
