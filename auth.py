import hashlib
import hmac
import os

from dbm import execute_query

def register_user(username, email, password):
    """Hashes the password and inserts a new user. Returns True on success."""
    password_hash = hash_password(password)
    result = execute_query(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username.strip(), email.strip(), password_hash),
    )
    return result is not None


def authenticate_user(username, password):
    """Verifies credentials and returns the user's id and username, or None."""
    rows = execute_query(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username.strip(),),
    )
    if rows and verify_password(password, rows[0]["password_hash"]):
        return {"id": rows[0]["id"], "username": rows[0]["username"]}
    return None

def hash_password(password):
    """Hashes a password using SHA-256 with a salt."""
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + pwd_hash  # Store salt + hash together

def verify_password(password, stored_hash):
    """Verifies a password against the stored hash."""
    salt = stored_hash[:16]
    stored_pwd_hash = stored_hash[16:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hmac.compare_digest(pwd_hash, stored_pwd_hash)

