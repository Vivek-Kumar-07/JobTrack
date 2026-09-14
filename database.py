import sqlite3


conn = sqlite3.connect("jobtrack.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")

import sqlite3

conn = sqlite3.connect("jobtrack.db")

conn.execute("""
ALTER TABLE applications
ADD COLUMN notes TEXT
""")

conn.commit()
conn.close()