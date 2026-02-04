import logging
import os
import datetime

class AppLogger:
    @staticmethod
    def setup():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        
        try:
            from src.common.config import DATA_DIR
            log_file = os.path.join(DATA_DIR, 'app.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.info(f"File logging enabled. Log file: {log_file}")
        except Exception as e:
            logging.error(f"Failed to setup file logging: {e}")

    @staticmethod
    def log(message, level="info"):
        if level == "info":
            logging.info(message)
        elif level == "error":
            logging.error(message)
        elif level == "warning":
            logging.warning(message)
