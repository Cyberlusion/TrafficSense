# Now you we import directly from data_ingestion without referring to individual modules:

from data_ingestion import start_mqtt_listener

# Update __init__.py for Easy Access
# the __init__.py file can aggregate imports for easier access:

from .processor import process_data
from .analyzer import analyze_traffic
from .stream_processor import start_stream_processing

__all__ = ["process_data", "analyze_traffic", "start_stream_processing"]
