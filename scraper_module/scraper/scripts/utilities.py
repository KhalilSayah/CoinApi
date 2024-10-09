import datetime


def format_data(data):
    return float(data.replace('\xa0','').replace('\n',''))

def add_days_to_date(start_date: str, days: int) -> str:
    """
    Returns the exact date after adding a number of days to the given start date.

    :param start_date: The start date in 'YYYY-MM-DD' format.
    :param days: The number of days to add to the start date.
    :return: The resulting date as a string in 'YYYY-MM-DD' format.
    """
    # Convert the start_date string to a datetime object
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

    # Add the specified number of days
    result_date = start_date_obj + datetime.timedelta(days=days)

    # Return the resulting date as a string
    return result_date.strftime('%Y-%m-%d')


def date_to_timestamp(date_str: str) -> int:
    """
    Converts a date string to a Unix timestamp.

    :param date_str: The date string in 'YYYY-MM-DD' format.
    :return: The Unix timestamp (seconds since epoch) as an integer.
    """
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Convert the datetime object to a Unix timestamp
    timestamp = int(date_obj.timestamp())

    return timestamp
