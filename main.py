
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uvicorn

from database import engine, Base
from auth.router import router as auth_router
from jobs.router import router as jobs_router
from applicants.router import router as applicants_router
from matching.router import router as matching_router
from interviews.router import router as interviews_router
from offers.router import router as offers_router
from applications.router import router as applications_router

# Create upload directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("offer_letters", exist_ok=True)

# Import all models to ensure they're registered
from auth.models import User, UserRole
from applicants.models import Applicant
from interviews.models import Interview, InterviewStatus
from offers.models import OfferLetter
from applications.models import JobApplication

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating database tables: {e}")

app = FastAPI(
    title="Recruitment Tracker System",
    description="A complete hiring management system with job postings, resume uploads, skill matching, interview scheduling, and offer letter generation.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for offer letters and UI
app.mount("/offer_letters", StaticFiles(directory="offer_letters"), name="offer_letters")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve CSS and JS files at root level for easier access
@app.get("/styles.css")
async def get_styles():
    return FileResponse("static/styles.css", media_type="text/css")

@app.get("/script.js")
async def get_script():
    return FileResponse("static/script.js", media_type="text/javascript")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
app.include_router(applicants_router, prefix="/applicants", tags=["Applicants"])
app.include_router(matching_router, prefix="/matching", tags=["Matching"])
app.include_router(interviews_router, prefix="/interviews", tags=["Interviews"])
app.include_router(offers_router, prefix="/offers", tags=["Offers"])
app.include_router(applications_router, prefix="/applications", tags=["Applications"])

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api")
async def api_root():
    return {"message": "Welcome to Recruitment Tracker System", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
