"""Initial migration: create all tables

Revision ID: 001
Revises: 
Create Date: 2026-06-17 15:34:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'student', name='userrole'), nullable=False, server_default='student'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_user_email', 'users', ['email'], unique=False)
    op.create_index('idx_user_role', 'users', ['role'], unique=False)
    op.create_index('idx_user_active', 'users', ['is_active'], unique=False)

    # Create students table
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('branch', sa.String(100), nullable=False),
        sa.Column('cgpa', sa.Float(), nullable=False),
        sa.Column('graduation_year', sa.Integer(), nullable=False),
        sa.Column('skills', sa.Text(), nullable=True),
        sa.Column('projects', sa.Text(), nullable=True),
        sa.Column('resume_url', sa.String(500), nullable=True),
        sa.Column('placement_readiness_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_student_user', 'students', ['user_id'], unique=True)
    op.create_index('idx_student_branch', 'students', ['branch'], unique=False)
    op.create_index('idx_student_cgpa', 'students', ['cgpa'], unique=False)

    # Create companies table
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('package_offered', sa.Float(), nullable=True),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('minimum_cgpa', sa.Float(), nullable=False),
        sa.Column('required_skills', sa.Text(), nullable=True),
        sa.Column('job_description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_company_name', 'companies', ['name'], unique=False)
    op.create_index('idx_company_location', 'companies', ['location'], unique=False)
    op.create_index('idx_company_active', 'companies', ['is_active', 'created_at'], unique=False)
    op.create_check_constraint('ck_cgpa_range', 'companies', "minimum_cgpa >= 0 AND minimum_cgpa <= 10")
    op.create_check_constraint('ck_package_positive', 'companies', 'package_offered IS NULL OR package_offered >= 0')

    # Create placement_drives table
    op.create_table(
        'placement_drives',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('drive_date', sa.DateTime(), nullable=False),
        sa.Column('application_deadline', sa.DateTime(), nullable=False),
        sa.Column('open_positions', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('draft', 'published', 'closed', name='drivestatus'), nullable=False, server_default='draft'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_drive_company', 'placement_drives', ['company_id'], unique=False)
    op.create_index('idx_drive_status', 'placement_drives', ['status'], unique=False)
    op.create_index('idx_drive_date', 'placement_drives', ['drive_date'], unique=False)
    op.create_check_constraint('ck_positions_positive', 'placement_drives', 'open_positions > 0')

    # Create applications table
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('drive_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('applied', 'shortlisted', 'interview_scheduled', 'selected', 'rejected', name='applicationstatus'), nullable=False, server_default='applied'),
        sa.Column('skill_match_percentage', sa.Float(), nullable=True),
        sa.Column('eligibility_status', sa.String(50), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('applied_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['drive_id'], ['placement_drives.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_application_student', 'applications', ['student_id'], unique=False)
    op.create_index('idx_application_drive', 'applications', ['drive_id'], unique=False)
    op.create_index('idx_application_status', 'applications', ['status'], unique=False)
    op.create_index('idx_application_student_status', 'applications', ['student_id', 'status'], unique=False)
    op.create_unique_constraint('uq_student_drive', 'applications', ['student_id', 'drive_id'])

    # Create assessments table
    op.create_table(
        'assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('total_marks', sa.Float(), nullable=False),
        sa.Column('passing_marks', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_assessment_active', 'assessments', ['is_active'], unique=False)

    # Create assessment_scores table
    op.create_table(
        'assessment_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('assessment_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('percentage', sa.Float(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_score_student', 'assessment_scores', ['student_id'], unique=False)
    op.create_index('idx_score_assessment', 'assessment_scores', ['assessment_id'], unique=False)
    op.create_unique_constraint('uq_student_assessment', 'assessment_scores', ['student_id', 'assessment_id'])


def downgrade() -> None:
    op.drop_table('assessment_scores')
    op.drop_table('assessments')
    op.drop_table('applications')
    op.drop_table('placement_drives')
    op.drop_table('companies')
    op.drop_table('students')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS drivestatus')
    op.execute('DROP TYPE IF EXISTS applicationstatus')