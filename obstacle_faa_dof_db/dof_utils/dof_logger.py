import logging


def custom_logger(logger_name, log_path):
    """ Custom logger for DOF import, conversion.
    :param logger_name: str
    :param log_path: str
    :return: Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(lineno)d | %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
