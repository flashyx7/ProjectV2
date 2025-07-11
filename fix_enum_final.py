
#!/usr/bin/env python3
"""
Final migration script to fix ApplicationStatus enum values and recreate the table.
This ensures complete consistency between database and application.
"""

import sqlite3
import os
from datetime import datetime

def fix_application_status_final():
    """Fix the ApplicationStatus enum values by recreating the table"""
    db_path = "recruitment_tracker.db"
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # First, backup existing data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_applications_backup AS 
            SELECT * FROM job_applications
        """)
        
        # Drop the existing table
        cursor.execute("DROP TABLE IF EXISTS job_applications")
        
        # Recreate the table with proper enum values
        cursor.execute("""
            CREATE TABLE job_applications (
                id INTEGER PRIMARY KEY,
                applicant_id INTEGER,
                job_id INTEGER,
                status VARCHAR(20) DEFAULT 'PENDING',
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(applicant_id) REFERENCES applicants(id),
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            )
        """)
        
        # Restore data with corrected status values
        cursor.execute("""
            INSERT INTO job_applications (id, applicant_id, job_id, status, applied_at)
            SELECT 
                id, 
                applicant_id, 
                job_id, 
                CASE 
                    WHEN status IN ('pending', 'PENDING') THEN 'PENDING'
                    WHEN status IN ('reviewed', 'REVIEWED') THEN 'REVIEWED'
                    WHEN status IN ('shortlisted', 'SHORTLISTED') THEN 'SHORTLISTED'
                    WHEN status IN ('rejected', 'REJECTED') THEN 'REJECTED'
                    ELSE 'PENDING'
                END as status,
                applied_at
            FROM job_applications_backup
        """)
        
        # Drop backup table
        cursor.execute("DROP TABLE job_applications_backup")
        
        # Commit changes
        conn.commit()
        print("Successfully recreated job_applications table with correct enum values!")
        
        # Verify the changes
        cursor.execute("SELECT DISTINCT status FROM job_applications")
        statuses = cursor.fetchall()
        print(f"Current status values: {statuses}")
        
    except Exception as e:
        print(f"Error fixing enum values: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_application_status_final()
