# NAINA VAI Backend - Render.com Deployment Guide

## Why Render.com?

✅ **Free tier** - No credit card required
✅ **Fast** - Good performance on free tier
✅ **Always online** - 24/7 availability
✅ **Auto-deploy** - Pushes from GitHub automatically deploy
✅ **Easy setup** - Simple configuration
✅ **HTTPS included** - Secure connections

---

## Quick Start (5 Minutes Setup)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `naina-vai-backend`
3. Make it **Public** (required for free tier)
4. Click "Create repository"

### Step 2: Upload Your Code to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. On your new repository page, click "uploading an existing file"
2. Drag and drop these files:
   - `backend_server.py`
   - `requirements.txt`
   - `render.yaml`
   - `.gitignore`
3. Click "Commit changes"

**Option B: Using Git Command Line**

```bash
# Initialize git in your project folder
git init
git add backend_server.py requirements.txt render.yaml .gitignore
git commit -m "Initial commit"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/naina-vai-backend.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. **Sign up for Render**
   - Go to https://render.com/
   - Click "Get Started for Free"
   - Sign up with GitHub (easiest option)

2. **Create New Web Service**
   - Click "New +" button (top right)
   - Select "Web Service"
   - Click "Build and deploy from a Git repository"
   - Click "Next"

3. **Connect Repository**
   - Click "Connect account" under GitHub
   - Authorize Render to access your repositories
   - Find and select `naina-vai-backend`
   - Click "Connect"

4. **Configure Service**
   
   Render will auto-detect settings from `render.yaml`, but verify:
   
   - **Name**: `naina-vai-backend` (or whatever you want)
   - **Region**: Choose closest to you (e.g., Singapore, Frankfurt, Oregon)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend_server:app`
   - **Instance Type**: `Free`

5. **Add Environment Variable**
   
   Scroll down to "Environment Variables" section:
   - Click "Add Environment Variable"
   - **Key**: `GROQ_API_KEY`
   - **Value**: Your actual Groq API key (get from https://console.groq.com/)
   - Click "Add"

6. **Deploy**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - You'll see build logs in real-time

### Step 4: Get Your Server URL

Once deployed (you'll see "Live" status):

1. Find your server URL at the top (looks like):
   ```
   https://naina-vai-backend.onrender.com
   ```

2. **Test it** - Click the URL or visit:
   ```
   https://naina-vai-backend.onrender.com/health
   ```
   
   You should see:
   ```json
   {"status": "Server is running"}
   ```

### Step 5: Update ESP32 Code

Update both ESP32 devices with your new cloud URL:

**ESP32-CAM (`esp32_cam_simple.ino`):**
```cpp
// OLD (local laptop)
const char* serverUrl = "http://10.140.171.191:5000/analyze";

// NEW (Render cloud)
const char* serverUrl = "https://naina-vai-backend.onrender.com/analyze";
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         Replace with YOUR Render URL
```

**ESP32 DevKit (`esp32_devkit_display.ino`):**
```cpp
// OLD (local laptop)
const char* serverUrl = "http://10.140.171.191:5000/get_result";

// NEW (Render cloud)
const char* serverUrl = "https://naina-vai-backend.onrender.com/get_result";
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         Replace with YOUR Render URL
```

**Important:** 
- Use `https://` (not `http://`)
- Don't include port number (no `:5000`)
- Use your actual Render URL

### Step 6: Upload and Test!

1. Upload updated code to both ESP32 devices
2. ESP32-CAM: Take a photo
3. ESP32 DevKit: Press REQUEST button
4. Should work from anywhere! 🎉

---

## Benefits of Cloud Deployment

### Before (Local Laptop):
- ❌ Laptop must be on and running
- ❌ Must be on same WiFi network
- ❌ IP address changes when you move
- ❌ Can't use when laptop is off/traveling

### After (Render Cloud):
- ✅ Always available 24/7
- ✅ Works from any WiFi network
- ✅ Fixed URL never changes
- ✅ No laptop needed
- ✅ Faster server response
- ✅ Can access from anywhere in the world

---

## Free Tier Limits

**Render Free Tier:**
- 750 hours/month (enough for 24/7)
- 512 MB RAM
- Sleeps after 15 min of inactivity
- Wakes up automatically on first request (takes ~30 seconds)
- 100 GB bandwidth/month

**Note:** First request after sleep will be slow (30 sec), but subsequent requests are instant.

**To prevent sleep (optional):**
- Upgrade to paid tier ($7/month)
- Or use a cron job to ping your server every 10 minutes

---

## Monitoring Your Deployment

### View Logs

1. Go to your Render dashboard
2. Click on your service
3. Click "Logs" tab
4. See real-time output (same as CMD window)

You'll see:
- Image received messages
- AI responses
- DevKit requests
- Any errors

### Check Status

Dashboard shows:
- **Live** - Service is running ✅
- **Build Failed** - Check logs for errors ❌
- **Deploying** - Deployment in progress 🔄

---

## Updating Your Code

Whenever you make changes:

1. **Update files on GitHub:**
   - Upload new files via web interface, OR
   - `git commit -am "Updated code"`
   - `git push`

2. **Render auto-deploys:**
   - Detects changes automatically
   - Rebuilds and redeploys
   - Takes 2-5 minutes
   - No downtime

---

## Troubleshooting

### Build Failed

**Check logs for:**
- Missing dependencies in `requirements.txt`
- Python syntax errors
- Import errors

**Solution:**
- Fix the error in your code
- Push to GitHub
- Render will auto-retry

### Service Won't Start

**Check:**
- Environment variable `GROQ_API_KEY` is set correctly
- Start command is: `gunicorn backend_server:app`
- Port is configured to use `PORT` env variable

### ESP32 Can't Connect

**Verify:**
- Using `https://` (not `http://`)
- Using correct Render URL
- No port number in URL
- ESP32 has internet access
- Server is "Live" in Render dashboard

### "Service Unavailable" Error

**Cause:** Service is waking up from sleep (free tier)

**Solution:** 
- Wait 30 seconds and try again
- First request after sleep is slow
- Subsequent requests are instant

### API Key Not Working

1. Go to Render dashboard
2. Click your service
3. Go to "Environment" tab
4. Check `GROQ_API_KEY` is set
5. Click "Save Changes" if you edited it

---

## Security Best Practices

✅ **DO:**
- Keep API key in Render environment variables (NOT in code)
- Use `.gitignore` to prevent sensitive files from uploading
- Monitor your Groq API usage

❌ **DON'T:**
- Commit API keys to GitHub
- Share your Render URL publicly (people could abuse it)
- Leave debug mode on in production

---

## Cost Comparison

| Option | Cost | Pros | Cons |
|--------|------|------|------|
| **Laptop** | Free (electricity) | Full control | Must stay on, same network |
| **Phone (Termux)** | Free | Portable | Battery drain, unreliable |
| **Render Free** | Free | 24/7, fast, reliable | Sleeps after 15 min |
| **Render Paid** | $7/month | No sleep, faster | Costs money |

**Recommendation:** Start with Render Free tier. Upgrade to paid only if the 30-second wake-up time bothers you.

---

## Alternative Cloud Providers

If you want to try others:

### **Railway.app**
- $5 free credit per month
- No sleep
- Easier setup
- https://railway.app/

### **Fly.io**
- Free tier available
- Global edge network
- More complex setup
- https://fly.io/

### **PythonAnywhere**
- Free tier
- Python-focused
- Limited bandwidth
- https://www.pythonanywhere.com/

**Verdict:** Render.com is the best balance of free + easy + fast for this project.

---

## Testing Your Deployment

### Test 1: Health Check
```bash
curl https://your-app.onrender.com/health
```
Should return: `{"status": "Server is running"}`

### Test 2: From Browser
Visit: `https://your-app.onrender.com/health`
Should see JSON response

### Test 3: From ESP32
1. ESP32-CAM: Take photo
2. Check Render logs for "Image received"
3. ESP32 DevKit: Request result
4. Should display on OLED!

---

## Useful Commands

### Check if server is running:
```bash
curl https://your-app.onrender.com/health
```

### View recent logs:
Go to Render Dashboard → Your Service → Logs

### Redeploy manually:
Render Dashboard → Your Service → Manual Deploy → Deploy Latest Commit

---

## Getting Help

**Render Documentation:**
- https://render.com/docs

**Groq API Docs:**
- https://console.groq.com/docs

**Common Issues:**
- Check Render logs first
- Verify environment variables
- Test with `/health` endpoint

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│ NAINA VAI - Render Deployment Quick Ref    │
├─────────────────────────────────────────────┤
│ 1. Create GitHub repo (public)              │
│ 2. Upload: backend_server.py, requirements, │
│           render.yaml, .gitignore           │
│ 3. Sign up: render.com                      │
│ 4. New Web Service → Connect repo           │
│ 5. Add env var: GROQ_API_KEY=your-key      │
│ 6. Deploy & wait 3-5 minutes                │
│ 7. Get URL: https://xxx.onrender.com        │
│ 8. Update ESP32 code with new URL          │
│ 9. Upload to ESP32s                         │
│ 10. Test and enjoy! 🚀                      │
└─────────────────────────────────────────────┘
```

---

## Success Checklist

- [ ] GitHub repository created
- [ ] Code uploaded to GitHub
- [ ] Render account created
- [ ] Web service deployed
- [ ] GROQ_API_KEY environment variable set
- [ ] Service shows "Live" status
- [ ] `/health` endpoint works
- [ ] ESP32-CAM code updated with Render URL
- [ ] ESP32 DevKit code updated with Render URL
- [ ] Both ESP32s uploaded and tested
- [ ] System working end-to-end!

---

**You're all set! Your NAINA VAI backend is now running in the cloud! ☁️🚀**

Created by Vishnu
