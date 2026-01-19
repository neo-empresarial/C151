import logging
import os
import datetime

class AppLogger:
    @staticmethod
    def setup():
        log_dir = "Logs"
        os.makedirs(log_dir, exist_ok=True)
        filename = f"log_{datetime.date.today()}.log"
        filepath = os.path.join(log_dir, filename)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(filepath),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def log(message, level="info"):
        if level == "info":
            logging.info(message)
        elif level == "error":
            logging.error(message)
        elif level == "warning":
            logging.warning(message)
