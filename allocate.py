from db_manager import execute_query, DAYS_PER_WEEK, PERIODS_PER_DAY

TOTAL_PERIODS = DAYS_PER_WEEK * PERIODS_PER_DAY

# A period counts as "taken" only when a row exists with a non-blank subject.
# Missing rows and rows with a NULL/blank subject both count as free.
_TAKEN = "s.subject IS NOT NULL AND TRIM(s.subject) <> ''"


def get_user_schedule(user_id):
    """Fetches the schedule for a specific user."""
    rows = execute_query(
        "SELECT day_of_week, period_number, subject FROM schedule WHERE user_id = ? ORDER BY day_of_week, period_number",
        (user_id,),
    )
    return [dict(row) for row in rows] if rows is not None else []


def get_all_schedules_by_user():
    """Fetches all schedule rows for all users."""
    rows = execute_query(
        "SELECT user_id, day_of_week, period_number, subject FROM schedule ORDER BY user_id, day_of_week, period_number"
    )
    return [dict(row) for row in rows] if rows is not None else []


def get_free_period_counts():
    """Returns every user with their number of free periods in the week,
    sorted by free periods (most first), then username.

    Each item: {"id", "username", "email", "free_periods", "assigned_periods"}.
    Users with no schedule rows are included with all periods free.
    """
    rows = execute_query(
        f"""
        SELECT u.id, u.username, u.email,
               COUNT(s.id) AS assigned_periods,
               {TOTAL_PERIODS} - COUNT(s.id) AS free_periods
        FROM users u
        LEFT JOIN schedule s ON s.user_id = u.id AND {_TAKEN}
        GROUP BY u.id
        ORDER BY free_periods DESC, u.username COLLATE NOCASE
        """
    )
    return [dict(row) for row in rows] if rows is not None else []


def list_user_by_free_period(day_of_week, period_number):
    """Lists users who are free on a specific day (1=Mon..5=Fri) and period (1..6)."""
    rows = execute_query(
        f"""
        SELECT u.id, u.username, u.email
        FROM users u
        LEFT JOIN schedule s
               ON s.user_id = u.id AND s.day_of_week = ? AND s.period_number = ? AND {_TAKEN}
        WHERE s.id IS NULL
        ORDER BY u.username COLLATE NOCASE
        """,
        (day_of_week, period_number),
    )
    return [dict(row) for row in rows] if rows is not None else []


if __name__ == '__main__':
    for u in get_free_period_counts():
        print(f"{u['username']:<20} {u['free_periods']:>2} free / {TOTAL_PERIODS}")
