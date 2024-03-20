import logging


def setup_logger(
    name: str,
    log_file: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure logging for the given name and log file with the specified level.

    :param name: The logger name.
    :param log_file: The log file path.
    :param level: The minimum logging level (INFO by default).
    :return: The configured logger instance.
    """

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger
