# OneLink Portfolio - Backend

A FastAPI backend for building auto-updated portfolios directly from GitHub data.

## Features

### 1. **GitHub OAuth Authentication**
- Secure GitHub OAuth 2.0 integration
- Automatic user profile creation
- Unique portfolio username generation
- Secure access token storage

### 2. **Automatic GitHub Sync**
- Fetch all public repositories
- Filter forked/archived repositories
- Extract programming languages
- Fetch README content
- Auto-detect live demo URLs

### 3. **Project Classification**
- Automatic status detection (deployed, code_only, in_progress)
- Demo URL detection from homepage/README
- Project stats (stars, forks, watchers)

### 4. **Resume Parsing**
- PDF & DOCX support
- Auto-extract skills, experience, education
- Structured data parsing

### 5. **Manual Profile Management**
- Add/edit work experience
- Education history
- Skills with proficiency levels
- Project media (screenshots, videos)

### 6. **Public Portfolio API**
- Shareable public portfolio links
- Privacy controls (show/hide projects)
- Portfolio visibility settings
- No authentication required for viewing

### 7. **Media Management**
- Project screenshots & videos
- GIF support
- Metadata storage
- Media ordering

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (with easy migration to PostgreSQL)
- **Auth**: JWT + GitHub OAuth
- **ORM**: SQLAlchemy 2.0
- **Resume Parsing**: PyPDF2, python-docx
- **HTTP**: HTTPX for async calls

## Setup

### 1. Create .env file

```bash
cp .env.example .env
```

Update with your GitHub OAuth credentials:

```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
SECRET_KEY=your_secret_key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

## API Endpoints

### Authentication
```
GET  /auth/login                    # Initiate GitHub OAuth login
GET  /auth/callback                 # OAuth callback handler
POST /auth/logout                   # Logout
```

### Users
```
GET    /users/me                       # Get current user profile
PUT    /users/me                       # Update user profile
GET    /users/{portfolio_username}     # Get public user profile

POST   /users/me/experience            # Add work experience
GET    /users/me/experience            # List experiences
PUT    /users/me/experience/{id}       # Update experience
DELETE /users/me/experience/{id}       # Delete experience

POST   /users/me/education             # Add education
GET    /users/me/education             # List education
PUT    /users/me/education/{id}        # Update education
DELETE /users/me/education/{id}        # Delete education

POST   /users/me/skills                # Add skill
GET    /users/me/skills                # List skills
PUT    /users/me/skills/{id}           # Update skill
DELETE /users/me/skills/{id}           # Delete skill
```

### Projects
```
POST   /projects/sync                  # Manual sync from GitHub
GET    /projects                       # List user's projects
GET    /projects/{id}                  # Get specific project
PUT    /projects/{id}                  # Update project (hide/show)
DELETE /projects/{id}                  # Delete project
```

### Resume
```
POST   /resume/upload                  # Upload & parse resume (PDF/DOCX)
GET    /resume/text                    # Get stored resume text
```

### Portfolio (Public)
```
GET    /portfolio/{portfolio_username} # Get public portfolio
```

### Health
```
GET    /health                         # Health check
GET    /                               # Root endpoint
```

## Database Schema

### Users
- `id`, `github_id`, `github_username`, `portfolio_username`
- `avatar_url`, `profile_url`, `bio`, `location`, `email`
- `access_token`, `resume_text`, `is_public`
- `created_at`, `updated_at`, `last_sync`

### Projects
- `id`, `github_id`, `user_id`
- `name`, `description`, `url`, `homepage`, `readme_content`
- `languages` (JSON), `stars`, `forks`, `watchers`
- `status` (deployed/code_only/in_progress)
- `is_deployed`, `deployed_url`, `is_visible`, `is_archived`, `is_fork`
- `created_at`, `updated_at`, `github_updated_at`

### Experience
- `id`, `user_id`, `title`, `company`, `location`
- `description`, `start_date`, `end_date`, `is_current`
- `created_at`, `updated_at`

### Education
- `id`, `user_id`, `school`, `degree`, `field_of_study`
- `description`, `start_date`, `end_date`, `is_current`
- `created_at`, `updated_at`

### Skills
- `id`, `user_id`, `name`, `proficiency`, `category`
- `created_at`, `updated_at`

### Media
- `id`, `user_id`, `project_id`
- `filename`, `file_path`, `media_type` (screenshot/video/gif)
- `mime_type`, `title`, `description`, `order`
- `created_at`, `updated_at`

## Authentication Flow

1. **User initiates login**
   ```
   GET /auth/login → Get OAuth URL
   ```

2. **User authenticates with GitHub**
   ```
   Redirect to GitHub consent screen
   ```

3. **GitHub redirects back**
   ```
   GET /auth/callback?code=...&state=...
   ```

4. **Backend exchanges code for token**
   ```
   → Returns JWT token + user info
   ```

5. **Use JWT for authenticated requests**
   ```
   Authorization: Bearer <jwt_token>
   ```

## GitHub Data Sync

### Automatic Sync Triggers
- On first login (via OAuth callback)
- Manual sync via `/projects/sync` endpoint
- Can be scheduled for periodic syncs

### What Gets Synced
- Repository name, description, URL
- Programming languages
- Stars, forks, watchers
- Homepage URL
- README content
- Project status (deployed/code-only/in-progress)
- Visibility status (archived, fork)

### Demo Detection
Automatically detects demo URLs from:
- Repository homepage field
- README links to: Vercel, Netlify, Render, Heroku, GitHub Pages, Surge

## Security Considerations

- ✅ GitHub access tokens stored securely
- ✅ JWT tokens with expiration
- ✅ CORS configured
- ✅ File upload validation
- ✅ Input sanitization
- ✅ SQLite foreign key constraints
- ⚠️ Use HTTPS in production
- ⚠️ Set secure SECRET_KEY
- ⚠️ Configure CORS properly for frontend

## Error Handling

All endpoints return standardized error responses:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

## Testing

```bash
# Run with auto-reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open API docs
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Development Notes

- Database: SQLite for MVP, easily migrate to PostgreSQL
- Models are in `app/models/`
- Schemas (validation) in `app/schemas/`
- Business logic in `app/services/`
- API routes in `app/api/`
- Configuration in `app/core/config.py`

## Future Enhancements (v2+)

- [ ] Project reordering
- [ ] Portfolio customization (themes)
- [ ] Comments/feedback on projects
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Rate limiting by IP
- [ ] Redis caching
- [ ] WebSocket real-time updates
- [ ] Admin panel
- [ ] Export portfolio as PDF
- [ ] Multi-language support

## License

MIT
