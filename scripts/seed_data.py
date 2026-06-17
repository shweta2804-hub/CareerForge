#!/usr/bin/env python3
"""
Seed data script for CareerForge.
Run this script to populate the database with sample data.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.company import Company
from app.models.placement_drive import PlacementDrive, DriveStatus
from app.models.assessment import Assessment
from app.core.security import get_password_hash


def get_seed_credentials():
    """Get credentials from environment variables or generate secure defaults."""
    admin_password = os.getenv("SEED_ADMIN_PASSWORD", "Admin@123")
    student_password = os.getenv("SEED_STUDENT_PASSWORD", "Student@123")
    
    # Warn if using default passwords
    if admin_password == "Admin@123":
        print("⚠️  WARNING: Using default admin password. Set SEED_ADMIN_PASSWORD env var for production.")
    if student_password == "Student@123":
        print("⚠️  WARNING: Using default student password. Set SEED_STUDENT_PASSWORD env var for production.")
    
    return admin_password, student_password


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def seed_users(db: Session):
    """Seed users."""
    admin_password, student_password = get_seed_credentials()
    
    users = [
        {
            "email": "admin@careerforge.com",
            "full_name": "Admin User",
            "hashed_password": get_password_hash(admin_password),
            "role": UserRole.ADMIN,
            "is_superuser": True,
        },
        {
            "email": "student1@careerforge.com",
            "full_name": "John Doe",
            "hashed_password": get_password_hash(student_password),
            "role": UserRole.STUDENT,
        },
        {
            "email": "student2@careerforge.com",
            "full_name": "Jane Smith",
            "hashed_password": get_password_hash(student_password),
            "role": UserRole.STUDENT,
        },
        {
            "email": "student3@careerforge.com",
            "full_name": "Bob Johnson",
            "hashed_password": get_password_hash(student_password),
            "role": UserRole.STUDENT,
        },
    ]

    for user_data in users:
        user = User(**user_data)
        db.add(user)
    
    db.commit()
    print(f"✓ Seeded {len(users)} users")


def seed_students(db: Session):
    """Seed student profiles."""
    students = [
        {
            "user_id": 2,
            "branch": "Computer Science",
            "cgpa": 8.5,
            "graduation_year": 2024,
            "skills": json.dumps(["Python", "SQL", "Docker", "Git", "React", "FastAPI"]),
            "projects": json.dumps([
                {"name": "E-commerce Platform", "tech": ["Python", "React", "PostgreSQL"]},
                {"name": "Chat Application", "tech": ["FastAPI", "WebSocket", "Redis"]},
            ]),
        },
        {
            "user_id": 3,
            "branch": "Information Technology",
            "cgpa": 9.0,
            "graduation_year": 2024,
            "skills": json.dumps(["Java", "Spring Boot", "MySQL", "AWS", "Docker"]),
            "projects": json.dumps([
                {"name": "Cloud Management System", "tech": ["Java", "AWS", "Docker"]},
            ]),
        },
        {
            "user_id": 4,
            "branch": "Computer Science",
            "cgpa": 7.8,
            "graduation_year": 2024,
            "skills": json.dumps(["Python", "Machine Learning", "TensorFlow", "SQL"]),
            "projects": json.dumps([
                {"name": "Image Classification", "tech": ["Python", "TensorFlow"]},
                {"name": "Sentiment Analysis", "tech": ["Python", "NLP"]},
            ]),
        },
    ]

    for student_data in students:
        student = Student(**student_data)
        db.add(student)
    
    db.commit()
    print(f"✓ Seeded {len(students)} student profiles")


def seed_companies(db: Session):
    """Seed companies."""
    companies = [
        {
            "name": "TechCorp Solutions",
            "package_offered": 12.5,
            "location": "Bangalore",
            "minimum_cgpa": 7.5,
            "required_skills": json.dumps(["Python", "SQL", "Docker", "Git"]),
            "job_description": "Looking for skilled software developers with strong Python and database skills.",
            "is_active": True,
        },
        {
            "name": "DataDriven Inc",
            "package_offered": 15.0,
            "location": "Hyderabad",
            "minimum_cgpa": 8.0,
            "required_skills": json.dumps(["Python", "Machine Learning", "SQL", "TensorFlow"]),
            "job_description": "Seeking data scientists and ML engineers for our analytics team.",
            "is_active": True,
        },
        {
            "name": "CloudFirst Technologies",
            "package_offered": 10.0,
            "location": "Pune",
            "minimum_cgpa": 7.0,
            "required_skills": json.dumps(["Java", "AWS", "Docker", "Spring Boot"]),
            "job_description": "Hiring cloud engineers and backend developers.",
            "is_active": True,
        },
        {
            "name": "InnovateLabs",
            "package_offered": 18.0,
            "location": "Mumbai",
            "minimum_cgpa": 8.5,
            "required_skills": json.dumps(["Python", "React", "FastAPI", "PostgreSQL", "Docker"]),
            "job_description": "Looking for full-stack developers for our innovative products.",
            "is_active": True,
        },
    ]

    for company_data in companies:
        company = Company(**company_data)
        db.add(company)
    
    db.commit()
    print(f"✓ Seeded {len(companies)} companies")


def seed_placement_drives(db: Session):
    """Seed placement drives."""
    drives = [
        {
            "company_id": 1,
            "drive_date": datetime.now() + timedelta(days=30),
            "application_deadline": datetime.now() + timedelta(days=15),
            "open_positions": 20,
            "status": DriveStatus.PUBLISHED,
            "description": "Software Developer positions at TechCorp Solutions",
        },
        {
            "company_id": 2,
            "drive_date": datetime.now() + timedelta(days=45),
            "application_deadline": datetime.now() + timedelta(days=20),
            "open_positions": 15,
            "status": DriveStatus.PUBLISHED,
            "description": "Data Scientist positions at DataDriven Inc",
        },
        {
            "company_id": 3,
            "drive_date": datetime.now() + timedelta(days=60),
            "application_deadline": datetime.now() + timedelta(days=30),
            "open_positions": 25,
            "status": DriveStatus.DRAFT,
            "description": "Cloud Engineer positions at CloudFirst Technologies",
        },
    ]

    for drive_data in drives:
        drive = PlacementDrive(**drive_data)
        db.add(drive)
    
    db.commit()
    print(f"✓ Seeded {len(drives)} placement drives")


def seed_assessments(db: Session):
    """Seed assessments."""
    assessments = [
        {
            "title": "Python Programming Test",
            "description": "Test your Python programming skills",
            "total_marks": 100,
            "passing_marks": 60,
            "is_active": True,
        },
        {
            "title": "Data Structures & Algorithms",
            "description": "Assess your DSA knowledge",
            "total_marks": 100,
            "passing_marks": 50,
            "is_active": True,
        },
        {
            "title": "SQL Proficiency Test",
            "description": "Test your SQL query writing skills",
            "total_marks": 50,
            "passing_marks": 30,
            "is_active": True,
        },
    ]

    for assessment_data in assessments:
        assessment = Assessment(**assessment_data)
        db.add(assessment)
    
    db.commit()
    print(f"✓ Seeded {len(assessments)} assessments")


def main():
    """Main seeding function."""
    print("\n" + "="*50)
    print("CareerForge Database Seeding")
    print("="*50 + "\n")

    try:
        # Create tables
        create_tables()

        # Create database session
        db = SessionLocal()

        # Seed data
        seed_users(db)
        seed_students(db)
        seed_companies(db)
        seed_placement_drives(db)
        seed_assessments(db)

        db.close()

        print("\n" + "="*50)
        print("✓ Database seeding completed successfully!")
        print("="*50 + "\n")

        admin_password, student_password = get_seed_credentials()
        
        print("Sample Credentials:")
        print("-" * 50)
        print("Admin:")
        print("  Email: admin@careerforge.com")
        print(f"  Password: {admin_password}")
        print("\nStudent:")
        print("  Email: student1@careerforge.com")
        print(f"  Password: {student_password}")
        print("-" * 50 + "\n")

    except Exception as e:
        print(f"\n✗ Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()