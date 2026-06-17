"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.connection import Base
from app.core.config import settings
import os

# Test database URL
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///./test.db"
)


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def auth_service(db: Session):
    """Create auth service instance."""
    from app.services.auth_service import AuthService
    return AuthService(db)


@pytest.fixture
def student_service(db: Session):
    """Create student service instance."""
    from app.services.student_service import StudentService
    return StudentService(db)


@pytest.fixture
def company_service(db: Session):
    """Create company service instance."""
    from app.services.company_service import CompanyService
    return CompanyService(db)


@pytest.fixture
def eligibility_engine():
    """Create eligibility engine instance."""
    from app.services.eligibility_engine import EligibilityEngine
    return EligibilityEngine()


@pytest.fixture
def skill_match_engine():
    """Create skill match engine instance."""
    from app.services.skill_match_engine import SkillMatchEngine
    return SkillMatchEngine()


@pytest.fixture
def readiness_score_service():
    """Create readiness score service instance."""
    from app.services.readiness_score_service import ReadinessScoreService
    return ReadinessScoreService()