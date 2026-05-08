# OneLink Portfolio 🚀

**Build your beautiful portfolio automatically from your GitHub profile**

**Status**: Production Ready | **Version**: 1.0.0 | **Full Stack Complete**

OneLink Portfolio is a complete full-stack application with a FastAPI backend and a static HTML/CSS/JS frontend. Automatically sync your GitHub repositories, build a stunning portfolio, and share it with the world.

---

## 🎯 Quick Navigation

### 👤 For Users
- **[QUICK_START.md](./QUICK_START.md)** - Setup in 5 minutes
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - All endpoints with examples

### 👨‍💻 For Developers
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Architecture & development guide
- **[backend/README.md](./backend/README.md)** - Technical documentation

### 📊 For Project Managers
- **[COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md)** - Features & status checklist

---

## ✨ What's Included

### 📦 Backend Code (30+ Files)

**API Endpoints** (21+ endpoints):
- ✅ GitHub OAuth authentication (2 endpoints)
- ✅ User management (3 endpoints)
- ✅ Experience/Education/Skills CRUD (9 endpoints)
- ✅ Project management & GitHub sync (7 endpoints)
- ✅ Resume upload & parsing (2 endpoints)
- ✅ Public portfolio API (1 endpoint)

**Database** (6 models):
- ✅ User (GitHub profile + portfolio data)
- ✅ Project (GitHub repos with tech stack)
- ✅ Experience (work history)
- ✅ Education (education history)
- ✅ Skill (skills & proficiency)
- ✅ Media (project media/screenshots)

**Services** (3 services):
- ✅ GitHub Service (repo fetching, demo detection)
- ✅ Resume Parser (PDF/DOCX support)
- ✅ Project Classifier (auto-tagging)

**Core** (4 modules):
- ✅ Config (environment variables)
- ✅ Security (JWT, OAuth, hashing)
- ✅ Database (SQLAlchemy ORM)
- ✅ Utilities (logging, helpers)

### 📚 Documentation (4 guides)

1. **QUICK_START.md** (6 KB)
   - 5-minute setup
   - Testing OAuth
   - Common issues

2. **API_DOCUMENTATION.md** (12 KB)
   - All endpoints documented
   - Request/response examples
   - Error codes
   - Rate limiting info

3. **IMPLEMENTATION_GUIDE.md** (15 KB)
   - Architecture overview
   - Development workflow
   - Database schema
   - Migration instructions

4. **COMPLETION_SUMMARY.md** (15 KB)
   - Feature checklist (15/15 ✅)
   - Implementation details
   - Security features
   - Deployment guide

### 🛠️ Configuration

- **backend/.env** - Environment configuration file
- **requirements.txt** - Python dependencies (v2.0 locked)
- **backend/README.md** - Backend overview

---

## 🚀 Getting Started (30 seconds)

```bash
# 1) Backend setup
cd backend
pip install -r requirements.txt

# 2) Create backend/.env (required)
cat > .env << 'EOF'
GITHUB_CLIENT_ID=your_github_app_id
GITHUB_CLIENT_SECRET=your_github_app_secret
GITHUB_OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
FRONTEND_CALLBACK_URL=http://localhost:3000/auth/sign-in.html
ALLOWED_ORIGINS=http://localhost:3000
SECRET_KEY=replace-with-a-strong-secret
EOF

# 3) Run backend API
uvicorn app.main:app --reload --port 8000

# 4) In another terminal, serve frontend
cd ../FRONTEND
python3 -m http.server 3000 --bind 0.0.0.0
```

---

## 📋 Feature Checklist (15/15 Complete)

- [x] GitHub OAuth login
- [x] User management
- [x] GitHub data fetching
- [x] Live demo detection
- [x] Project classification
- [x] Resume parsing
- [x] Manual profile data
- [x] Project media support
- [x] Public portfolio API
- [x] Auto sync logic
- [x] Privacy controls
- [x] API structure
- [x] Database design
- [x] Security measures
- [x] Health & utilities

---

## 💻 Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0
- **Auth**: python-jose (JWT) + GitHub OAuth
- **Database**: SQLite (production-ready for PostgreSQL)
- **File Parsing**: PyPDF2, python-docx
- **HTTP**: HTTPX (async)

---

## 🔐 Security Features

- ✅ GitHub OAuth 2.0
- ✅ JWT tokens with expiration
- ✅ Pydantic input validation
- ✅ File upload validation
- ✅ SQL injection prevention (ORM)
- ✅ CORS protection
- ✅ Environment-based secrets
- ✅ Foreign key constraints

---

## 📁 Project Structure

```
onelink-portfolio/
├── backend/
│   ├── app/
│   │   ├── api/              (5 modules, 21+ endpoints)
│   │   ├── models/           (6 database models)
│   │   ├── schemas/          (4 validation modules)
│   │   ├── services/         (3 business logic modules)
│   │   ├── core/             (config, security, db)
│   │   └── main.py           (FastAPI app setup)
│   ├── requirements.txt      (locked versions)
│   └── README.md             (technical docs)
├── FRONTEND/                 (static frontend app)
├── QUICK_START.md            (setup guide)
├── API_DOCUMENTATION.md      (endpoint reference)
├── IMPLEMENTATION_GUIDE.md   (development guide)
├── COMPLETION_SUMMARY.md     (feature checklist)
└── README.md                 (this file)
```

---

## 🌐 API Overview

### Authentication
```
GET  /auth/login              # Get GitHub OAuth URL
GET  /auth/callback           # OAuth callback
POST /auth/logout             # Logout
```

### Users
```
GET  /users/me                # Get profile
PUT  /users/me                # Update profile
GET  /users/{username}        # Get public profile
```

### Experience/Education/Skills
```
POST   /users/me/experience   # Add experience
GET    /users/me/experience   # List experience
PUT    /users/me/experience/{id}
DELETE /users/me/experience/{id}

POST   /users/me/education    # Add education
GET    /users/me/education    # List education
PUT    /users/me/education/{id}
DELETE /users/me/education/{id}

POST   /users/me/skills       # Add skill
GET    /users/me/skills       # List skills
PUT    /users/me/skills/{id}
DELETE /users/me/skills/{id}
```

### Projects
```
POST   /projects/sync         # Manual GitHub sync
GET    /projects              # List user's projects
GET    /projects/{id}         # Get project
PUT    /projects/{id}         # Update project
DELETE /projects/{id}         # Delete project
```

### Resume
```
POST   /resume/upload         # Upload & parse resume
GET    /resume/text           # Get resume text
```

### Portfolio (Public)
```
GET    /portfolio/{username}  # View public portfolio (no auth!)
```

---

## 🧪 Testing

### Interactive API Testing
```
http://localhost:8000/docs    # Swagger UI
http://localhost:8000/redoc   # ReDoc
```

### Manual Testing
1. Click "Authorize" → Complete GitHub OAuth
2. Test any endpoint directly in UI
3. Get instant responses with examples

### Example Flow
```bash
# Get OAuth URL
curl http://localhost:8000/auth/login

# After OAuth callback, get token
# Then sync projects
curl -X POST http://localhost:8000/projects/sync \
  -H "Authorization: Bearer <token>"

# View public portfolio
curl http://localhost:8000/portfolio/yourusername
```

---

## 🚀 Deployment

### Development
```bash
uvicorn app.main:app --reload
```

### Production (Example: Railway)
```bash
# Push to GitHub
# Connect Railway
# Set environment variables
# Deploy!
```

### Docker
```bash
docker build -t onelink-backend .
docker run -p 8000:8000 onelink-backend
```

### Database
- MVP: SQLite (included)
- Production: PostgreSQL (configuration ready)

---

## 📊 Code Statistics

| Metric | Value |
|--------|-------|
| Python Files | 30+ |
| API Endpoints | 21+ |
| Database Models | 6 |
| Services | 3 |
| Lines of Code | ~3000 |
| Documentation | 4 guides |

---

## ✅ What Works Out of the Box

- ✅ GitHub OAuth login flow
- ✅ Automatic project syncing
- ✅ Resume parsing (PDF/DOCX)
- ✅ User profile management
- ✅ Experience/education/skills management
- ✅ Public portfolio viewing
- ✅ Demo URL detection
- ✅ Project visibility control
- ✅ Database persistence
- ✅ Error handling & logging
- ✅ Input validation
- ✅ Auto-generated API docs

---

## 🔧 Configuration

Core configuration through `backend/.env`:

```env
# GitHub OAuth
GITHUB_CLIENT_ID=your_id
GITHUB_CLIENT_SECRET=your_secret
GITHUB_OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback

# JWT
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
DB_NAME=onelink_portfolio.db

# Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=uploads
```

## ⚠️ OAuth Callback URL Must Match Exactly

If GitHub shows: `The redirect_uri is not associated with this application`, verify these are an exact match:

1. GitHub OAuth App callback URL
2. `GITHUB_OAUTH_REDIRECT_URI` in `backend/.env`
3. Backend callback route (`/auth/callback`)

Expected local value:

```text
http://localhost:8000/auth/callback
```

---

## 📈 Performance

- Async/await throughout
- Connection pooling ready
- Pagination support
- Efficient database queries
- GitHub API rate limit aware
- File streaming support

---

## 🎓 Learning Resources

### For API Integration
See: **API_DOCUMENTATION.md**
- Complete endpoint reference
- Request/response examples
- Error codes
- Pagination info

### For Backend Development
See: **IMPLEMENTATION_GUIDE.md**
- Architecture overview
- Database schema details
- Authentication flow
- Development workflow

### For Quick Setup
See: **QUICK_START.md**
- 5-minute setup
- Common issues
- Testing steps

---

## 🔒 Security Checklist

- ✅ GitHub credentials in .env (not in code)
- ✅ JWT token validation on every request
- ✅ Pydantic input sanitization
- ✅ File type validation
- ✅ SQL injection prevention (ORM)
- ✅ CORS configured
- ✅ Password hashing (when needed)
- ✅ Rate limiting framework ready

---

## 🎉 Next Steps

### For Users/Testers
1. Run backend (see QUICK_START.md)
2. Test OAuth login
3. Sync GitHub projects
4. Upload resume
5. View public portfolio

### For Frontend Developers
1. Read API_DOCUMENTATION.md
2. Use Swagger UI for testing
3. Implement frontend integration
4. Handle OAuth callback
5. Build UI components

### For DevOps/Deployment
1. Configure PostgreSQL (if needed)
2. Setup environment variables
3. Create Docker image
4. Deploy to hosting platform
5. Setup monitoring

---

## 📞 Support

### Endpoints
- **Root**: http://localhost:8000/
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### Documentation
- QUICK_START.md - Setup
- API_DOCUMENTATION.md - Endpoints
- IMPLEMENTATION_GUIDE.md - Development
- COMPLETION_SUMMARY.md - Features

### Issues
- Check logs: `uvicorn app.main:app --reload --log-level debug`
- Verify .env configuration
- Check GitHub OAuth settings
- Read error messages in API responses

---

## 📝 License

MIT

---

## 🙏 Summary

**OneLink Portfolio Backend is complete and ready for:**

✅ Frontend integration
✅ User testing
✅ Production deployment
✅ Customization & extension
✅ Mobile app backend
✅ Open source contribution

**Start with**: [QUICK_START.md](./QUICK_START.md)

---

**Created**: February 5, 2026
**Status**: ✅ Production Ready
**All Features**: 15/15 Implemented
