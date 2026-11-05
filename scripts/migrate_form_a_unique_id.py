import sqlite3
import os
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "app.db"

def migrate():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(ProductionLog)")
    cols = [row[1] for row in cursor.fetchall()]
    
    if "form_unique_id" not in cols:
        print("Adding form_unique_id column to ProductionLog...")
        cursor.execute("ALTER TABLE ProductionLog ADD COLUMN form_unique_id VARCHAR(100)")
        cursor.execute("UPDATE ProductionLog SET form_unique_id = '007824' WHERE id = 1 AND form_unique_id IS NULL")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_ProductionLog_form_unique_id ON ProductionLog(form_unique_id)")
        conn.commit()
        print("Migration completed: form_unique_id added with UNIQUE index.")
    else:
        print("Column form_unique_id already exists.")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_ProductionLog_form_unique_id ON ProductionLog(form_unique_id)")
        conn.commit()

    cursor.execute("PRAGMA table_info(ProductionLog)")
    print("Current schema:", cursor.fetchall())
    conn.close()

if __name__ == "__main__":
    migrate()
