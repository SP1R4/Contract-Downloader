import logging
import json_log_formatter

def setup_logging():
    formatter = json_log_formatter.JSONFormatter()

    json_handler = logging.FileHandler(filename="contract_downloader.log")
    json_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(json_handler)
    logger.addHandler(console_handler)

    return logger
