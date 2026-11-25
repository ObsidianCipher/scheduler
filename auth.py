import hashlib
import hmac
import os

from db_manager import execute_query

PBKDF2_ITERATIONS = 600_000


def register_user(username, email, password):
    """Hashes the password and inserts a new user. Returns True on success."""
    password_hash = hash_password(password)
    result = execute_query(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username.strip(), email.strip(), password_hash),
    )
    return result is not None


def authenticate_user(username, password):
    """Verifies credentials and returns the user's id, username and role, or None."""
    rows = execute_query(
        "SELECT id, username, role, password_hash FROM users WHERE username = ?",
        (username.strip(),),
    )
    if rows and verify_password(password, rows[0]["password_hash"]):
        return {"id": rows[0]["id"], "username": rows[0]["username"], "role": rows[0]["role"]}
    return None


def hash_password(password):
    """Hashes a password with PBKDF2-HMAC-SHA256 and a random salt."""
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_ITERATIONS)
    return salt + pwd_hash  # Store salt + hash together (bytes -> BLOB column)


def verify_password(password, stored_hash):
    """Verifies a password against the stored hash."""
    stored_hash = bytes(stored_hash)
    salt = stored_hash[:16]
    stored_pwd_hash = stored_hash[16:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(pwd_hash, stored_pwd_hash)
