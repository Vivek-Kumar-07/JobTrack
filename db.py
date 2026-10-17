import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DATABASE = os.path.join(BASE_DIR, "jobtrack.db")


def uses_postgresql():
    return bool(os.environ.get("DATABASE_URL"))

def get_integrity_error():
    if uses_postgresql():
        import psycopg2
        return psycopg2.IntegrityError

    return sqlite3.IntegrityError

def current_timestamp_sql():
    if uses_postgresql():
        return "CURRENT_TIMESTAMP"
    return "datetime('now')"

def monthly_date_sql():
    if uses_postgresql():
        return "TO_CHAR(TO_DATE(date, 'YYYY-MM-DD'), 'YYYY-MM')"

    return "strftime('%Y-%m', date)"


def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        import psycopg2
        from psycopg2.extras import DictCursor

        conn = psycopg2.connect(database_url)
        return PostgreSQLConnection(conn, DictCursor)

    conn = sqlite3.connect(SQLITE_DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def convert_placeholders(query):
    """Convert SQLite ? placeholders outside SQL quoted text."""
    result = []
    quote = None
    i = 0

    while i < len(query):
        char = query[i]

        if quote:
            result.append(char)

            if char == quote:
                # SQL escapes quotes by doubling them.
                if i + 1 < len(query) and query[i + 1] == quote:
                    result.append(query[i + 1])
                    i += 2
                    continue
                quote = None

        elif char in ("'", '"'):
            quote = char
            result.append(char)

        elif char == "?":
            result.append("%s")

        else:
            result.append(char)

        i += 1

    return "".join(result)


class PostgreSQLConnection:
    """Small adapter for the existing conn.execute() pattern."""

    def __init__(self, connection, cursor_factory):
        self.connection = connection
        self.cursor_factory = cursor_factory

    def execute(self, query, params=()):
        # Convert the existing SQLite-style placeholders.
        query = convert_placeholders(query)

        cursor = self.connection.cursor(
            cursor_factory=self.cursor_factory
        )
        cursor.execute(query, params)
        return cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
