# Aggregating Submodules for Cleaner Imports
#In a package with multiple submodules, you might want to gather all components in __init__.py to simplify imports elsewhere in the project.

from .db_handler import connect_db, insert_data, query_data
from .schema import TrafficDataSchema

__all__ = ["connect_db", "insert_data", "query_data", "TrafficDataSchema"]
