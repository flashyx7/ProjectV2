
import os
import sys
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine, Base
from auth.models import User, UserRole
from jobs.models import JobPosition
from applicants.models import Applicant
from interviews.models import Interview, InterviewStatus
from offers.models import OfferLetter
from bcrypt import hashpw, gensalt

def create_sample_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(OfferLetter).delete()
        db.query(Interview).delete()
        db.query(Applicant).delete()
        db.query(Job).delete()
        db.query(User).delete()
        db.commit()
        
        # Create sample users
        company_user = User(
            username="company_hr",
            hashed_password=hashpw("password123".encode('utf-8'), gensalt()).decode('utf-8'),
            role=UserRole.company,
            is_active=True
        )
        
        applicant_user1 = User(
            username="john_doe",
            hashed_password=hashpw("password123".encode('utf-8'), gensalt()).decode('utf-8'),
            role=UserRole.applicant,
            is_active=True
        )
        
        applicant_user2 = User(
            username="jane_smith",
            hashed_password=hashpw("password123".encode('utf-8'), gensalt()).decode('utf-8'),
            role=UserRole.applicant,
            is_active=True
        )
        
        db.add_all([company_user, applicant_user1, applicant_user2])
        db.commit()
        db.refresh(company_user)
        db.refresh(applicant_user1)
        db.refresh(applicant_user2)
        
        # Create sample jobs
        jobs = [
            JobPosition(
                title="Senior Python Developer",
                description="We are looking for an experienced Python developer to join our team. You will be responsible for developing web applications using FastAPI and Django.",
                skills=["Python", "FastAPI", "Django", "PostgreSQL", "REST API"],
                salary=95000.0,
                location="New York, NY",
                company_id=company_user.id
            ),
            JobPosition(
                title="Frontend React Developer",
                description="Join our frontend team to build amazing user interfaces using React and modern JavaScript technologies.",
                skills=["React", "JavaScript", "TypeScript", "CSS", "HTML"],
                salary=75000.0,
                location="San Francisco, CA",
                company_id=company_user.id
            ),
            JobPosition(
                title="Data Scientist",
                description="Analyze large datasets and build machine learning models to drive business insights.",
                skills=["Python", "Machine Learning", "Pandas", "NumPy", "SQL"],
                salary=110000.0,
                location="Remote",
                company_id=company_user.id
            ),
            JobPosition(
                title="DevOps Engineer",
                description="Manage cloud infrastructure and CI/CD pipelines for our applications.",
                skills=["AWS", "Docker", "Kubernetes", "Jenkins", "Python"],
                salary=105000.0,
                location="Austin, TX",
                company_id=company_user.id
            ),
            Job(
                title="Full Stack Developer",
                description="Work on both frontend and backend development using modern technologies.",
                skills=["React", "Node.js", "Python", "MongoDB", "Express"],
                salary=85000.0,
                location="Seattle, WA",
                company_id=company_user.id
            )
        ]
        
        db.add_all(jobs)
        db.commit()
        
        # Refresh to get IDs
        for job in jobs:
            db.refresh(job)
        
        # Create sample applicants
        applicants = [
            Applicant(
                name="John Doe",
                email="john.doe@email.com",
                phone="555-0123",
                resume_path="uploads/john_doe_resume.pdf",
                skills=["Python", "FastAPI", "PostgreSQL", "REST API", "Git"],
                total_experience=5,
                user_id=applicant_user1.id
            ),
            Applicant(
                name="Jane Smith", 
                email="jane.smith@email.com",
                phone="555-0456",
                resume_path="uploads/jane_smith_resume.pdf",
                skills=["React", "JavaScript", "TypeScript", "CSS", "Node.js"],
                total_experience=3,
                user_id=applicant_user2.id
            ),
            Applicant(
                name="Mike Johnson",
                email="mike.johnson@email.com",
                phone="555-0789",
                resume_path="uploads/mike_johnson_resume.pdf",
                skills=["Python", "Machine Learning", "Pandas", "NumPy", "TensorFlow"],
                total_experience=7,
                user_id=None
            ),
            Applicant(
                name="Sarah Wilson",
                email="sarah.wilson@email.com",
                phone="555-0321",
                resume_path="uploads/sarah_wilson_resume.pdf",
                skills=["AWS", "Docker", "Kubernetes", "Python", "Linux"],
                total_experience=4,
                user_id=None
            ),
            Applicant(
                name="David Brown",
                email="david.brown@email.com",
                phone="555-0654",
                resume_path="uploads/david_brown_resume.pdf",
                skills=["React", "Node.js", "MongoDB", "Express", "JavaScript"],
                total_experience=6,
                user_id=None
            )
        ]
        
        db.add_all(applicants)
        db.commit()
        
        # Refresh to get IDs
        for applicant in applicants:
            db.refresh(applicant)
        
        # Create sample interviews
        interviews = [
            Interview(
                applicant_id=applicants[0].id,
                position_id=jobs[0].id,
                date_time=datetime.now() + timedelta(days=3, hours=10),
                status=InterviewStatus.scheduled
            ),
            Interview(
                applicant_id=applicants[1].id,
                position_id=jobs[1].id,
                date_time=datetime.now() + timedelta(days=5, hours=14),
                status=InterviewStatus.scheduled
            ),
            Interview(
                applicant_id=applicants[2].id,
                position_id=jobs[2].id,
                date_time=datetime.now() + timedelta(days=1, hours=16),
                status=InterviewStatus.scheduled
            ),
            Interview(
                applicant_id=applicants[3].id,
                position_id=jobs[3].id,
                date_time=datetime.now() - timedelta(days=2, hours=11),
                status=InterviewStatus.completed
            ),
            Interview(
                applicant_id=applicants[4].id,
                position_id=jobs[4].id,
                date_time=datetime.now() + timedelta(days=7, hours=9),
                status=InterviewStatus.scheduled
            )
        ]
        
        db.add_all(interviews)
        db.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📝 Test Credentials:")
        print("Company/HR User:")
        print("  Username: company_hr")
        print("  Password: password123")
        print("\nApplicant Users:")
        print("  Username: john_doe")
        print("  Password: password123")
        print("  Username: jane_smith") 
        print("  Password: password123")
        print(f"\n📊 Created:")
        print(f"  - {len([company_user, applicant_user1, applicant_user2])} users")
        print(f"  - {len(jobs)} job positions")
        print(f"  - {len(applicants)} applicants")
        print(f"  - {len(interviews)} interviews")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
