__all__ = ["TimeIntervals"]

class TimeIntervals:
    """Class containing time intervals in seconds."""
    ONE_MIN_IN_SEC = 60                       # 1 minute in seconds
    ONE_HOUR_IN_SEC = ONE_MIN_IN_SEC * 60     # 1 hour in seconds
    ONE_DAY_IN_SEC = ONE_HOUR_IN_SEC * 24     # 1 day in seconds
    ONE_WEEK_IN_SEC = ONE_DAY_IN_SEC * 7      # 1 week in seconds
    ONE_MONTH_IN_SEC = 60 * 60 * 24 * 30      # 1 month (30 days) in seconds
    ONE_MONTH_IN_DAYS = 30                    # 1 month in days (assuming 30 days in a month)