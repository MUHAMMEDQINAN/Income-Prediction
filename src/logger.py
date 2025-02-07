from datetime import datetime
import logging
import os


# Creating a Timestamped Log File Name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# eg : 02_07_2025_12_30_45.log
# Ensures each log file has a unique name based on the timestamp.


# Creates a log file path inside the "logs" folder.
log_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
# eg: /home/user/income_prediction/logs/02_07_2025_12_30_45.log

# Creating the Logs Directory (if it doesn’t exist)
os.makedirs(os.path.dirname(log_path),exist_ok=True)

# Configuring Logging Settings
logging.basicConfig(
    # specifies the log file to write logs
    filename = log_path,
    # define how log message will be formatted
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)

## Just to verify logging works
# if __name__ == "__main__":
#     logging.info("Logging Started")