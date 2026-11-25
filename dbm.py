# This file is the backend database manager for the application. It is responsible for managing the database connection and providing an interface for the application to interact with the database.
# Donot edit this file unless you are sure of what you are doing. Any changes made to this file should be reported.
#The intial prototype will be using SQLite as the database. However, the code is designed to be easily adaptable to other databases in the future.
# Gateway to 2 dbs : users, schedule 

import sqlite3

def get_db_connection():
    """Establishes a connection to the SQLite database with foreign keys enabled."""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def close_db_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()


def initialize_database():
    """Initializes the database by creating necessary tables if they don't exist."""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                        password_hash TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        role TEXT NOT NULL DEFAULT 'user'  -- Added role column with default value
                    ) STRICT;
                ''')
                # Change BETWEEN 1 AND 6 to BETWEEN 1 AND 5 if restricting to Monday-Friday
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS schedule (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 6),
                        period_number INTEGER NOT NULL CHECK (period_number BETWEEN 1 AND 6),
                        subject TEXT,
                        UNIQUE (user_id, day_of_week, period_number),
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    ) STRICT;
                ''')
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            close_db_connection(conn)


def execute_query(query, params=()):
    """Executes a SQL query with optional parameters and returns fetched rows."""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn:
                cursor = conn.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return None
        finally:
            close_db_connection(conn)

def initialize_database():
    """Initializes the database by creating necessary tables if they don't exist."""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                        password_hash TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ) STRICT;
                ''')
                # Restricted to 5 days (1 = Monday to 5 = Friday) and 6 periods
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS schedule (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 5),
                        period_number INTEGER NOT NULL CHECK (period_number BETWEEN 1 AND 6),
                        subject TEXT,
                        UNIQUE (user_id, day_of_week, period_number),
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    ) STRICT;
                ''')
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            close_db_connection(conn)




def set_period(user_id, day_of_week, period_number, subject):
    """Inserts or updates a single period (day 1-5, period 1-6) for a user."""
    result = execute_query(
        """
        INSERT INTO schedule (user_id, day_of_week, period_number, subject)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (user_id, day_of_week, period_number)
        DO UPDATE SET subject = excluded.subject
        """,
        (user_id, day_of_week, period_number, subject),
    )
    return result is not None


def get_weekly_schedule(user_id):
    """Returns a user's full Mon-Fri schedule sorted by day and period."""
    rows = execute_query(
        """
        SELECT day_of_week, period_number, subject
        FROM schedule
        WHERE user_id = ?
        ORDER BY day_of_week, period_number
        """,
        (user_id,),
    )
    return [dict(row) for row in rows] if rows is not None else []

