import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "jobtrack.db")

conn = sqlite3.connect(DATABASE)

# Create applications table if it doesn't exist
conn.execute("""
CREATE TABLE IF NOT EXISTS applications (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company TEXT NOT NULL,

    role TEXT NOT NULL,

    status TEXT NOT NULL,

    date TEXT NOT NULL,

    notes TEXT,

    interview_date TEXT,

    interview_time TEXT,

    interview_type TEXT,

    follow_up_date TEXT,

    company_url TEXT,

    job_url TEXT

)
""")


# Check which columns already exist
columns = conn.execute(
    "PRAGMA table_info(applications)"
).fetchall()

existing_columns = [column[1] for column in columns]


# Add Phase 2 columns if they don't already exist

if "notes" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN notes TEXT"
    )

if "interview_date" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN interview_date TEXT"
    )

if "interview_time" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN interview_time TEXT"
    )

if "interview_type" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN interview_type TEXT"
    )

if "follow_up_date" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN follow_up_date TEXT"
    )

if "company_url" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN company_url TEXT"
    )

if "job_url" not in existing_columns:
    conn.execute(
        "ALTER TABLE applications ADD COLUMN job_url TEXT"
    )


# Status History Table

conn.execute("""
CREATE TABLE IF NOT EXISTS status_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    application_id INTEGER NOT NULL,

    status TEXT NOT NULL,

    changed_at TEXT NOT NULL,

    FOREIGN KEY (application_id)
        REFERENCES applications(id)

)
""")

# Users Table

conn.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

)
""")


# Add user_id column to applications table

columns = conn.execute(
    "PRAGMA table_info(applications)"
).fetchall()

existing_columns = [column[1] for column in columns]

if "user_id" not in existing_columns:

    conn.execute(
        "ALTER TABLE applications ADD COLUMN user_id INTEGER"
    )


conn.commit()
conn.close()

print("Database updated successfully!")