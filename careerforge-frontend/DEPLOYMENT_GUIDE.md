# CareerForge Frontend - Render Deployment Guide

## Quick Start: Deploy in 5 Minutes

### Prerequisites
- GitHub account
- Render account (free at render.com)
- Backend already deployed at https://careerforge-tw8t.onrender.com

---

## Step-by-Step Deployment

### Step 1: Prepare Repository

```bash
# Navigate to frontend directory
cd careerforge-frontend

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial CareerForge frontend deployment"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/careerforge-frontend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Create Static Site on Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Static Site**
   - Click "New +" button (top right)
   - Select "Static Site"
   - Click "Connect" next to your GitHub account

3. **Select Repository**
   - Find `careerforge-frontend` repository
   - Click "Connect"

### Step 3: Configure Build Settings

Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `careerforge-frontend` |
| **Branch** | `main` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `dist` |
| **Node Version** | `18` |

### Step 4: Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add these three variables:

| Key | Value |
|-----|-------|
| `NODE_VERSION` | `18` |
| `VITE_API_URL` | `https://careerforge-tw8t.onrender.com` |
| `VITE_APP_NAME` | `CareerForge` |

**Important**: 
- Variable names are case-sensitive
- `VITE_API_URL` must start with `VITE_` for Vite to expose it
- No quotes around values

### Step 5: Deploy

1. Click "Create Static Site"
2. Wait for build to complete (2-3 minutes)
3. Watch the build logs for any errors
4. Once complete, you'll see your live URL

**Your frontend will be live at**: `https://careerforge-frontend.onrender.com`

---

## Post-Deployment Verification

### Immediate Checks (First 5 Minutes)

#### 1. Frontend Loads ✅
- [ ] Visit your Render URL
- [ ] Page loads completely
- [ ] No blank screen
- [ ] Styling appears correctly
- [ ] No console errors (F12 → Console)

#### 2. Routing Works ✅
Test these URLs directly (type in browser):
- [ ] `https://your-url.onrender.com/` → Redirects to login
- [ ] `https://your-url.onrender.com/login` → Shows login page
- [ ] `https://your-url.onrender.com/register` → Shows register page
- [ ] `https://your-url.onrender.com/dashboard` → Redirects to login (not 404)
- [ ] Refresh on any page → Still works (not 404)

**Critical**: If any route shows 404, the rewrite rule isn't working. Check `render.yaml`.

#### 3. Backend Communication ✅
1. Open DevTools (F12)
2. Go to Network tab
3. Try to login with test credentials
4. Check that API calls go to: `https://careerforge-tw8t.onrender.com`
5. No CORS errors in console
6. No 404 errors on API endpoints

#### 4. Login Works ✅
- [ ] Go to `/login`
- [ ] Enter valid credentials
- [ ] Click "Sign in"
- [ ] Redirects to `/dashboard`
- [ ] User name appears in header
- [ ] Token stored (check Application → Local Storage)

#### 5. Registration Works ✅
- [ ] Go to `/register`
- [ ] Fill in all fields
- [ ] Submit form
- [ ] Auto-login after registration
- [ ] Redirects to dashboard

#### 6. Dashboard Loads ✅
- [ ] Stats cards display
- [ ] Quick actions visible
- [ ] Sidebar navigation works
- [ ] No console errors
- [ ] Loading spinners work

#### 7. All Pages Load ✅
Click through each page in sidebar:
- [ ] Companies → Page loads
- [ ] Placement Drives → Page loads
- [ ] Applications → Page loads
- [ ] Assessments → Page loads
- [ ] Analytics → Page loads (admin only)

---

## Common Issues & Solutions

### Issue: Build Fails

**Symptoms**: Build shows errors in Render logs

**Solutions**:
1. Check Node.js version is 18
2. Verify `package.json` is valid
3. Try building locally first: `npm run build`
4. Check for missing dependencies

### Issue: 404 on Routes

**Symptoms**: Direct URL access shows 404

**Solutions**:
1. Verify `render.yaml` exists in root
2. Check rewrite rule is present:
   ```yaml
   routes:
     - type: rewrite
       source: /*
       destination: /index.html
   ```
3. Redeploy after fixing

### Issue: API Calls Fail

**Symptoms**: CORS errors, 404 on API endpoints

**Solutions**:
1. Verify `VITE_API_URL` in Render environment variables
2. Check backend is running: https://careerforge-tw8t.onrender.com/docs
3. Update backend CORS to allow frontend domain
4. Check browser console for specific errors

### Issue: Login Doesn't Work

**Symptoms**: Login button does nothing, or redirects back to login

**Solutions**:
1. Check Network tab for failed API calls
2. Verify API URL is correct
3. Test backend login endpoint directly
4. Check CORS configuration
5. Verify JWT token is being returned

### Issue: Environment Variables Not Working

**Symptoms**: API URL is undefined, app name wrong

**Solutions**:
1. Ensure variables start with `VITE_`
2. Redeploy after changing variables
3. Check Render dashboard for correct values
4. Variables are injected at build time, not runtime

---

## Updating the Deployment

### Automatic Deployments

Every push to `main` branch triggers automatic deployment:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically:
1. Detect the push
2. Run build command
3. Deploy if build succeeds

### Manual Deploy

In Render dashboard:
1. Go to your static site
2. Click "Manual Deploy" → "Deploy latest commit"

### Rollback

If something breaks:
1. Go to Render dashboard
2. Click "Deploys" tab
3. Find previous successful deploy
4. Click "Rollback to this deploy"

---

## Custom Domain (Optional)

### Add Custom Domain

1. In Render dashboard, go to your static site
2. Click "Settings" → "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `careerforge.com`)
5. Follow DNS configuration instructions

### DNS Configuration

Add these records to your DNS provider:

| Type | Host | Value |
|------|------|-------|
| CNAME | `www` | `careerforge-frontend.onrender.com` |
| A | `@` | (Render's IP) |

Or use Render's nameservers for easier setup.

---

## Monitoring & Maintenance

### Check Deployment Status

**Render Dashboard**:
- View build logs
- Check deployment history
- Monitor bandwidth usage
- See error rates

**Browser Console**:
- Check for JavaScript errors
- Monitor network requests
- Verify API responses

### Update Dependencies

```bash
# Update package.json versions
npm update

# Test locally
npm run build

# Commit and push
git add .
git commit -m "Update dependencies"
git push origin main
```

---

## Performance Optimization

### Already Configured
- ✅ Vite code splitting
- ✅ Asset minification
- ✅ CSS purging (Tailwind)
- ✅ Gzip compression (Render)
- ✅ CDN delivery (Render)

### Additional Optimizations (Optional)

1. **Enable Caching**
   - Render automatically sets cache headers
   - Static assets cached for 1 year

2. **Image Optimization**
   - Use WebP format
   - Lazy load images
   - Responsive images

3. **Code Splitting**
   - Implement React.lazy() for routes
   - Dynamic imports for heavy components

---

## Security Checklist

- [x] HTTPS enabled (automatic on Render)
- [x] Environment variables not in git
- [x] No secrets in client-side code
- [x] CORS configured on backend
- [x] XSS protection (React handles this)
- [x] Content Security Policy (can be added)

---

## Cost Estimate

### Render Free Tier
- **Static Sites**: Free
- **Bandwidth**: 100 GB/month
- **Builds**: Unlimited
- **Custom Domains**: Free

**Total Cost**: $0/month (within free tier limits)

### When to Upgrade
- > 100 GB bandwidth/month
- Need faster builds
- Need priority support

---

## Success Checklist

### Deployment Complete When:
- [x] Build succeeds on Render
- [x] Frontend URL is accessible
- [x] All routes work (including refresh)
- [x] Login works with backend
- [x] Registration works
- [x] Dashboard loads
- [x] All pages load
- [x] No console errors
- [x] API calls succeed
- [x] No CORS errors

---

## Next Steps After Deployment

1. **Test Everything**
   - Login/Register
   - All pages
   - All user flows
   - Mobile responsiveness

2. **Share with Team**
   - Send Render URL
   - Share test credentials
   - Request feedback

3. **Monitor**
   - Check Render logs daily
   - Monitor for errors
   - Track usage

4. **Iterate**
   - Fix any issues
   - Add missing features
   - Improve UI/UX

---

## Support Resources

### Documentation
- Render Static Sites: https://render.com/docs/static-sites
- Vite Deployment: https://vitejs.dev/guide/static-deploy.html
- React Router: https://reactrouter.com/en/main/start/overview

### Troubleshooting
- Render Community: https://community.render.com
- Render Status: https://status.render.com

---

## 🎉 Deployment Complete!

Once all checks pass, your CareerForge frontend is live and ready for users!

**Live URL**: `https://careerforge-frontend.onrender.com`
**Backend API**: `https://careerforge-tw8t.onrender.com`
**API Docs**: `https://careerforge-tw8t.onrender.com/docs`

---

## Quick Reference

### Important URLs
- Frontend: https://careerforge-frontend.onrender.com
- Backend: https://careerforge-tw8t.onrender.com
- API Docs: https://careerforge-tw8t.onrender.com/docs
- Render Dashboard: https://dashboard.render.com

### Important Files
- `render.yaml` - Deployment configuration
- `package.json` - Dependencies
- `vite.config.ts` - Build configuration
- `.env.example` - Environment variables template

### Build Command
```bash
npm install && npm run build
```

### Local Development
```bash
npm install
npm run dev
```

---

**Deployment Status**: ✅ READY
**Estimated Time**: 5-10 minutes
**Difficulty**: Easy
**Cost**: Free