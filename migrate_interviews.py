
import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('recruitment_tracker.db')
cursor = conn.cursor()

try:
    # Check if created_at column already exists
    cursor.execute("PRAGMA table_info(interviews)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'created_at' not in columns:
        # For SQLite, we need to add the column without a default
        cursor.execute("ALTER TABLE interviews ADD COLUMN created_at DATETIME")
        
        # Update existing records with current timestamp
        cursor.execute("UPDATE interviews SET created_at = datetime('now') WHERE created_at IS NULL")
        
        conn.commit()
        print("✅ Successfully added created_at column to interviews table")
    else:
        print("ℹ️  created_at column already exists")
        
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
