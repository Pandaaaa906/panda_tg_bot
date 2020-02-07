import logging


FORMAT = '[%(asctime)s] %(levelname)s in %(funcName)s: %(message)s'
formatter = logging.Formatter(FORMAT)
default_handler = logging.StreamHandler()
default_handler.setFormatter(formatter)


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logs.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(default_handler)
    logger.addHandler(file_handler)
    return logger
