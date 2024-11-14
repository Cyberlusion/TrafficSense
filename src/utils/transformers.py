#Data Transformation Functions

#If you need to transform data (e.g., converting timestamps, normalizing values, or reformatting data for display), you can put those functions here.

# src/utils/transformers.py
from datetime import datetime

def format_timestamp(timestamp: str) -> str:
    """
    Formats the timestamp string into a standard format.
    
    :param timestamp: Timestamp string to format.
    :return: Formatted timestamp.
    """
    try:
        # Assuming timestamp is in the format 'YYYY-MM-DD HH:MM:SS'
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.isoformat()  # Convert to ISO format
    except ValueError:
        return None

def normalize_data(value: float, min_value: float, max_value: float) -> float:
    """
    Normalizes a value to a range of [0, 1].

    :param value: The value to normalize.
    :param min_value: The minimum value in the data.
    :param max_value: The maximum value in the data.
    :return: Normalized value.
    """
    return (value - min_value) / (max_value - min_value) if max_value != min_value else 0
