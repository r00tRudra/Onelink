# OneLink Authentication & Data Loading Guide

## Issue Summary
The frontend dashboard was showing null/0 values for all profile details because users didn't have a valid JWT token stored in localStorage.
Rudra i am 

## How It Works (Normal Flow)

```
Landing Page (index.html)
    ↓ User clicks "Sign in"
Sign-in Page (auth/sign-in.html) 
    ↓ User clicks "GitHub" button
Backend Auth Endpoint (http://localhost:8000/auth/login)
    ↓ Redirects to GitHub OAuth
GitHub OAuth Consent Screen
    ↓ User authorizes
GitHub Callback to Backend (http://localhost:8000/auth/callback?code=...&state=...)
    ↓ Backend validates code, creates JWT token, creates/updates user in database
Redirect to Frontend (http://localhost:3000/auth/sign-in.html?token=...&user_id=...&username=...)
    ↓ Frontend extracts token from URL
Store in localStorage + Fetch user profile
    ↓ Redirect to dashboard with token in localStorage
Dashboard (pages/dashboard.html)
    ↓ Load with authenticated API calls
Display user data and projects
```

## Testing the Application

### Option 1: Using the Test Login Page (Quick Testing)
The fastest way to test is to bypass GitHub OAuth:
hello world

### Debugging the Authentication Flow

#### Check if Token is in localStorage
Open browser DevTools Console and run:
```javascript
localStorage.getItem('access_token')
```

Should return a JWT token starting with `eyJ...`

#### Check if User Data is in localStorage
```javascript
JSON.parse(localStorage.getItem('auth_user'))
```

Should return the user object with fields like `github_username`, `portfolio_username`, `email`, etc.

#### Check Browser Console for Errors
Open browser DevTools → Console tab and look for messages prefixed with:
- `[DEBUG]` - Shows API calls and responses
- `[ERROR]` - Shows errors
- `[AUTH]` - Shows authentication flow details

#### Test API Endpoints Directly
From browser DevTools Console:
```javascript
// Get user profile
fetch('http://localhost:8000/users/me', {
  headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
}).then(r => r.json()).then(console.log)

// Get projects
fetch('http://localhost:8000/projects', {
  headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
}).then(r => r.json()).then(console.log)
```

## Common Issues and Solutions

### Issue: Dashboard shows "Error" with loading spinner
**Cause**: Token is missing or invalid
**Solution**: 
- Check localStorage for access_token
- Try logging out and logging back in through GitHub OAuth
- Or use test-login.html for quick testing

fghijk
abcd e

give me that 
removed the guide 
