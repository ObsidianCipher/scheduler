from dbm import execute_query
import datetime

def get_user_schedule(user_id):
    """Fetches the schedule for a specific user."""
    rows = execute_query(
        "SELECT day_of_week, period_number, subject FROM schedule WHERE user_id = ? ORDER BY day_of_week, period_number",
        (user_id,),
    )
    return [dict(row) for row in rows] if rows is not None else []

def get_all_free_schedules_by_user():
    """Fetches all schedules for all users."""
    rows = execute_query(
        "SELECT user_id, day_of_week, period_number, subject FROM schedule ORDER BY user_id, day_of_week, period_number"
    )
    return [dict(row) for row in rows] if rows is not None else []

def list_user_by_free_period(period_number):
    """Lists users who are free during a specific day and period."""
    day_of_week = datetime.now().isoweekday()  # Get current day of the week (1=Monday, 7=Sunday)
    rows = execute_query(
        """
        SELECT u.id, u.username, u.email
        FROM users u
        LEFT JOIN schedule s ON u.id = s.user_id AND s.day_of_week = ? AND s.period_number = ?
        WHERE s.subject IS NULL
        """,
        (day_of_week, period_number),
    )
    return [dict(row) for row in rows] if rows is not None else []