#Data Validation Functions

#You may want to validate the incoming data, such as checking whether a value is a valid number, ensuring data types are correct, or confirming that required fields are present.

# src/utils/data_validator.py

from typing import Any

def validate_data(data: dict, required_fields: list) -> bool:
    """
    Validates if the given data contains all the required fields.

    :param data: The data dictionary to validate.
    :param required_fields: A list of field names that are required.
    :return: True if all required fields are present, else False.
    """
    for field in required_fields:
        if field not in data:
            return False
    return True

def validate_number(value: Any) -> bool:
    """
    Validates if a value is a valid number.

    :param value: The value to check.
    :return: True if it's a valid number, else False.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
