# CareerForge - Placement Portal

A modern, full-stack placement portal built with React, TypeScript, and FastAPI. CareerForge streamlines the placement process for students, companies, and administrators.

![Status](https://img.shields.io/badge/status-production-success)
![Backend](https://img.shields.io/badge/backend-online-success)
![Frontend](https://img.shields.io/badge/frontend-ready-blue)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## ✨ Features

### For Students
- 📝 **Profile Management** - Create and update student profiles
- 📄 **Resume Upload** - Upload and manage resumes
- 🏢 **Browse Companies** - View registered companies
- 📅 **Placement Drives** - Apply for campus drives
- 📊 **Application Tracking** - Track application status
- 📈 **Analytics** - View placement statistics

### For Administrators
- 🏢 **Company Management** - Add and manage companies
- 📅 **Drive Management** - Create and manage placement drives
- 👥 **Student Management** - View and manage students
- 📊 **Analytics Dashboard** - Comprehensive analytics
- ✅ **Application Review** - Review and process applications

### For Companies
- 📋 **Drive Posting** - Post placement drives
- 👀 **Application Review** - Review student applications
- 📊 **Analytics** - View drive statistics

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with OAuth2
- **Migrations**: Alembic
- **API Docs**: Swagger/OpenAPI

### Frontend
- **Framework**: React 18
- **Language**: TypeScript 5
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3
- **Forms**: React Hook Form + Zod
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Notifications**: React Hot Toast

### Infrastructure
- **Hosting**: Render
- **Database**: Neon PostgreSQL
- **Storage**: Cloudinary (planned)
- **CI/CD**: GitHub Actions

---

## 📁 Project Structure

```
CareerForge/
├── backend/                    # Backend application
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── repositories/      # Data access layer
│   │   ├── core/              # Configuration
│   │   ├── database/          # Database connection
│   │   └── middleware/        # Custom middleware
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
├── frontend/                   # Frontend application
│   └── careerforge-frontend/
│       ├── src/
│       │   ├── pages/         # Page components
│       │   ├── components/    # Reusable components
│       │   ├── contexts/      # React contexts
│       │   ├── services/      # API services
│       │   └── index.css      # Global styles
│       ├── package.json       # Node dependencies
│       └── render.yaml        # Render config
│
├── docs/                       # Documentation
│   └── reports/                # Audit & verification reports
│       ├── deployment/         # Deployment reports
│       ├── verification/       # Verification reports
│       ├── audit/              # Audit reports
│       └── frontend/           # Frontend reports
│
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Backend container
├── render.yaml                 # Render deployment
├── requirements.txt            # Backend dependencies
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and secrets

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend
cd frontend/careerforge-frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your API URL

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## 📚 Documentation

### Main Documentation
- **README.md** - This file (project overview)
- **docs/deployment/** - Deployment guides
- **docs/api/** - API specifications

### Reports & Audits
- **docs/reports/deployment/** - Deployment reports
- **docs/reports/verification/** - Runtime & functional verification
- **docs/reports/audit/** - Code audits & analysis
- **docs/reports/frontend/** - Frontend implementation reports

### Quick Links
- [Deployment Guide](docs/deployment/RENDER_DEPLOYMENT_GUIDE.md)
- [API Documentation](https://careerforge-tw8t.onrender.com/docs)
- [Frontend Repository](https://github.com/yourusername/careerforge-frontend)

---

## 🌐 Deployment

### Live URLs
- **Backend API**: https://careerforge-tw8t.onrender.com
- **API Docs**: https://careerforge-tw8t.onrender.com/docs
- **Frontend**: https://careerforge-frontend.onrender.com (when deployed)

### Deployment Platforms
- **Backend**: Render (Web Service)
- **Frontend**: Render (Static Site)
- **Database**: Neon PostgreSQL

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:5173","https://careerforge-frontend.onrender.com"]
```

#### Frontend (.env)
```env
VITE_API_URL=https://careerforge-tw8t.onrender.com
VITE_APP_NAME=CareerForge
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend/careerforge-frontend
npm run test
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **CareerForge Team** - Initial work

---

## 📞 Support

For support, email support@careerforge.com or open an issue in the repository.

---

## 🎯 Roadmap

- [x] Backend API development
- [x] Frontend development
- [x] Authentication system
- [x] Database integration
- [x] Deployment on Render
- [ ] Email notifications
- [ ] Resume parsing
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Multi-language support

---

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- React and Vite for the frontend tooling
- Tailwind CSS for the styling framework
- Render for hosting
- Neon for PostgreSQL database

---

**Built with ❤️ for CareerForge**