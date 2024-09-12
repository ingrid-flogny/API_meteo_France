import logging
import os

# Ensure the logs directory exists
log_directory = "./logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_directory, "app.log")),
        logging.StreamHandler(),  # Optional: to also print logs to the console
    ],
)
logger = logging.getLogger(__name__)
