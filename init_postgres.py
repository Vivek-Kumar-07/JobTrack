
import os
import psycopg2


def initialize_postgres():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL must be set to initialize PostgreSQL."
        )

    conn = psycopg2.connect(database_url)

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id BIGSERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS applications (
                        id BIGSERIAL PRIMARY KEY,
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
                        job_url TEXT,
                        user_id BIGINT
                            REFERENCES users(id)
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS status_history (
                        id BIGSERIAL PRIMARY KEY,
                        application_id BIGINT NOT NULL
                            REFERENCES applications(id),
                        status TEXT NOT NULL,
                        changed_at TIMESTAMP NOT NULL
                            DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS
                    idx_applications_user_date
                    ON applications(user_id, date)
                """)

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS
                    idx_applications_user_status
                    ON applications(user_id, status)
                """)

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS
                    idx_applications_user_followup
                    ON applications(user_id, follow_up_date)
                """)

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS
                    idx_status_history_application
                    ON status_history(application_id)
                """)

    finally:
        conn.close()


if __name__ == "__main__":
    initialize_postgres()
    print("PostgreSQL schema initialized successfully.")
