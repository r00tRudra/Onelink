# OneLink Authentication & Data Loading Guide


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
   

Should return a JWT token starting with `eyJ...`



give me that 
removed the guide 
