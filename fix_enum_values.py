
#!/usr/bin/env python3
"""
Migration script to fix ApplicationStatus enum values in the database.
Converts lowercase enum values to uppercase to match the enum definition.
"""

import sqlite3
import os

def fix_application_status_enum():
    """Fix the ApplicationStatus enum values in the database"""
    db_path = "recruitment_tracker.db"
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if job_applications table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='job_applications'
        """)
        
        if not cursor.fetchone():
            print("job_applications table not found.")
            return
        
        # Get all current status values
        cursor.execute("SELECT DISTINCT status FROM job_applications")
        current_statuses = cursor.fetchall()
        print(f"Current status values: {current_statuses}")
        
        # Update lowercase values to uppercase
        status_mappings = {
            'pending': 'PENDING',
            'reviewed': 'REVIEWED',
            'shortlisted': 'SHORTLISTED',
            'rejected': 'REJECTED'
        }
        
        for old_status, new_status in status_mappings.items():
            cursor.execute("""
                UPDATE job_applications 
                SET status = ? 
                WHERE status = ?
            """, (new_status, old_status))
            
            updated_rows = cursor.rowcount
            if updated_rows > 0:
                print(f"Updated {updated_rows} rows from '{old_status}' to '{new_status}'")
        
        # Commit the changes
        conn.commit()
        print("Successfully updated all enum values!")
        
        # Verify the changes
        cursor.execute("SELECT DISTINCT status FROM job_applications")
        new_statuses = cursor.fetchall()
        print(f"New status values: {new_statuses}")
        
    except Exception as e:
        print(f"Error fixing enum values: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_application_status_enum()
