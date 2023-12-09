import os
import sys
import logging
import datetime

# create log folder and file
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_dir, "logs")
log_file_name = f"{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_file = os.path.join(log_dir, log_file_name)
os.makedirs(log_dir, exist_ok=True)

# setup logging
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"

# add basic config
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("RSGISToolBoxLogger")
