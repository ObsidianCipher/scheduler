"""
Role Hierarchy and Access Control Module
Role Hierarchy:
- Admin: Full access to all functionalities, including user management and schedule management.
- Head: Access to manage schedules and view user data, but cannot manage users.
- User (teacher): Limited access, primarily to manage their own schedule and view their own data.

Access Control Functions:
- access_identifier(user_id): Fetches the role of the user based on their user_id.
- is_admin(user_id): Checks if the user has an admin role.
- change_user_role(user_id, new_role): Changes the role of a user. Returns True on success.
- get_all_users(): Fetches all users and their roles.
- is_head_or_admin(user_id): Checks if the user has a head or admin role.

"""

from db_manager import execute_query, VALID_ROLES


def access_identifier(user_id):
    """Fetches the role of the user based on their user_id."""
    rows = execute_query(
        "SELECT role FROM users WHERE id = ?",
        (user_id,),
    )
    if rows:
        return rows[0]["role"]
    return None


def is_admin(user_id):
    """Checks if the user has an admin role."""
    return access_identifier(user_id) == 'admin'


def is_head_or_admin(user_id):
    """Checks if the user has a head or admin role."""
    return access_identifier(user_id) in ('head', 'admin')


def change_user_role(user_id, new_role):
    """Changes the role of a user. Returns True on success, False if the role
    is invalid, the user doesn't exist, or the update fails.

    Callers must check is_admin(acting_user_id) before calling this.
    """
    if new_role not in VALID_ROLES or access_identifier(user_id) is None:
        return False
    result = execute_query(
        "UPDATE users SET role = ? WHERE id = ?",
        (new_role, user_id),
    )
    return result is not None


def get_all_users():
    """Fetches all users and their roles."""
    rows = execute_query(
        "SELECT id, username, email, role FROM users",
    )
    return [dict(row) for row in rows] if rows is not None else []
