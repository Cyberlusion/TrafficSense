#logger.py: Centralized Logging Utility
#A good logging setup is essential for debugging and tracking the behavior of your application. 
#Python's logging module can be used to create a central logger that can be used across the project.

# src/utils/logger.py
import logging

# Setting up a logger
def setup_logger(name: str, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create a stream handler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Create a file handler to log into a file (optional)
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Example usage:
logger = setup_logger("traffic_data_logger")
