import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "app.db"

def migrate():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in cursor.fetchall()]

    if "plain_password" not in cols:
        print("Adding plain_password column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN plain_password VARCHAR(255)")
        cursor.execute("UPDATE users SET plain_password = 'admin123' WHERE username = 'admin'")
        cursor.execute("UPDATE users SET plain_password = '123456' WHERE username = 'adnan1'")
        cursor.execute("UPDATE users SET plain_password = 'Jatin@16' WHERE username = 'Jatin'")
        conn.commit()
        print("Migration complete: plain_password column added.")
    else:
        print("plain_password column already exists.")

    cursor.execute("PRAGMA table_info(users)")
    print("Columns:", [r[1] for r in cursor.fetchall()])
    cursor.execute("SELECT employee_id, username, plain_password FROM users")
    print("Users:", cursor.fetchall())
    conn.close()

if __name__ == "__main__":
    migrate()
