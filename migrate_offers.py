
import sqlite3
import os

def migrate_offers():
    db_path = "recruitment_tracker.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if offers table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='offers'")
        if not cursor.fetchone():
            print("❌ Offers table not found")
            return
        
        # Check current columns
        cursor.execute("PRAGMA table_info(offers)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add salary column if it doesn't exist
        if 'salary' not in columns:
            cursor.execute("ALTER TABLE offers ADD COLUMN salary REAL")
            print("✅ Added salary column to offers table")
        
        # Add start_date column if it doesn't exist
        if 'start_date' not in columns:
            cursor.execute("ALTER TABLE offers ADD COLUMN start_date TEXT")
            print("✅ Added start_date column to offers table")
        
        conn.commit()
        print("✅ Offers table migration completed successfully")
        
    except Exception as e:
        print(f"❌ Error migrating offers table: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_offers()
