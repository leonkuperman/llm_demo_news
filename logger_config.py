# logger_config.py
import logging

# Configure logging to output only to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs to console only
    ]
)

# Function to get a named logger
def get_logger(name):
    return logging.getLogger(name)