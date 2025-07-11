#!/usr/bin/env python3

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from auth.models import User
from applicants.models import Applicant
from jobs.models import JobPosition
from interviews.models import Interview
from offers.models import OfferLetter
from applications.models import JobApplication

def create_tables():
    # Drop all tables first to ensure clean schema
    Base.metadata.drop_all(bind=engine)
    # Create all tables with current schema
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()