# CareerForge

Cloud-based placement and career readiness platform for colleges and training institutes.

## Features

- **Authentication & Authorization**: JWT-based auth with role-based access (Admin/Student)
- **Student Management**: Profile management, resume upload, skills tracking
- **Company Management**: Company profiles, requirements, and job descriptions
- **Placement Drives**: Create and manage placement drives with status tracking
- **Application System**: Apply to drives, track status, and manage applications
- **Eligibility Engine**: Automatic eligibility checking based on CGPA and skills
- **Skill Match Engine**: Dynamic skill matching with percentage calculation
- **Placement Readiness Score**: Calculated score (0-100) with category classification
- **Assessment Module**: Create assessments and record student scores
- **Analytics Dashboard**: Comprehensive placement statistics and insights
- **Email Notifications**: Automated emails for drives, applications, and status updates
- **Resume Management**: Cloudinary-based PDF resume storage

## Architecture

- **Clean Architecture**: Separation of concerns with repositories, services, and endpoints
- **Tech Stack**: FastAPI, SQLAlchemy 2.0, PostgreSQL, Pydantic v2
- **Pattern**: Repository pattern, Service layer pattern, Dependency injection
- **API Versioning**: `/api/v1` prefix for all endpoints

## Project Structure

```
careerforge/
├── app/
│   ├── api/v1/endpoints/    # API route handlers
│   ├── core/                # Configuration and security
│   ├── database/            # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── dependencies/        # FastAPI dependencies
│   ├── middleware/          # Custom middleware
│   └── main.py              # Application entry point
├── alembic/                 # Database migrations
├── tests/                   # Test files
└── .github/workflows/       # CI/CD pipelines
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CareerForge
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Docker

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT secret key | Yes |
| `ALGORITHM` | JWT algorithm (default: HS256) | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry (default: 30) | No |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes (for resume upload) |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes (for resume upload) |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes (for resume upload) |
| `SMTP_HOST` | Email SMTP host | No |
| `SMTP_PORT` | Email SMTP port | No |
| `SMTP_USER` | Email username | No |
| `SMTP_PASSWORD` | Email password | No |

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

### Students
- `POST /api/v1/students/profile` - Create student profile
- `GET /api/v1/students/profile` - Get student profile
- `PUT /api/v1/students/profile` - Update student profile
- `POST /api/v1/students/resume` - Upload resume
- `GET /api/v1/students/all` - Get all students (admin)
- `GET /api/v1/students/{id}` - Get student by ID (admin)

### Companies
- `POST /api/v1/companies` - Create company (admin)
- `GET /api/v1/companies` - Get all companies
- `GET /api/v1/companies/{id}` - Get company by ID
- `PUT /api/v1/companies/{id}` - Update company (admin)
- `DELETE /api/v1/companies/{id}` - Delete company (admin)
- `GET /api/v1/companies/search/{name}` - Search companies

### Placement Drives
- `POST /api/v1/drives` - Create drive (admin)
- `GET /api/v1/drives` - Get all drives
- `GET /api/v1/drives/published` - Get published drives
- `GET /api/v1/drives/{id}` - Get drive by ID
- `PUT /api/v1/drives/{id}` - Update drive (admin)
- `POST /api/v1/drives/{id}/publish` - Publish drive (admin)
- `POST /api/v1/drives/{id}/close` - Close drive (admin)
- `DELETE /api/v1/drives/{id}` - Delete drive (admin)

### Applications
- `POST /api/v1/applications` - Apply to drive
- `GET /api/v1/applications/my-applications` - Get my applications
- `GET /api/v1/applications/drive/{id}` - Get drive applications (admin)
- `GET /api/v1/applications/{id}` - Get application by ID
- `PUT /api/v1/applications/{id}/status` - Update status (admin)
- `GET /api/v1/applications` - Get all applications (admin)

### Assessments
- `POST /api/v1/assessments` - Create assessment (admin)
- `GET /api/v1/assessments` - Get all assessments
- `GET /api/v1/assessments/{id}` - Get assessment by ID
- `PUT /api/v1/assessments/{id}` - Update assessment (admin)
- `DELETE /api/v1/assessments/{id}` - Delete assessment (admin)
- `POST /api/v1/assessments/{id}/submit` - Submit assessment score
- `GET /api/v1/assessments/my-scores` - Get my scores
- `GET /api/v1/assessments/{id}/scores` - Get assessment scores (admin)

### Analytics
- `GET /api/v1/analytics/overview` - Get overview stats (admin)
- `GET /api/v1/analytics/top-companies` - Get top hiring companies (admin)
- `GET /api/v1/analytics/branch-stats` - Get branch-wise stats (admin)
- `GET /api/v1/analytics/full-report` - Get complete report (admin)

## Deployment

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add all variables from `.env.example`

### Using Docker

```bash
# Build image
docker build -t careerforge .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/careerforge \
  -e SECRET_KEY=your-secret-key \
  careerforge
```

## Sample Credentials

After running seed data:

**Admin User:**
- Email: admin@careerforge.com
- Password: Admin@123

**Student User:**
- Email: student@careerforge.com
- Password: Student@123

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app
```

## Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking (optional)
mypy app/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request