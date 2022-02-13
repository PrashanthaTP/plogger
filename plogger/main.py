import logging
from os import path as os_path

logging.basicConfig(format="[%(levelname)s]  %(name)s | %(lineno)s : %(msg)s")


def __get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    fmt = "[%(levelname)s] %(name)s | %(lineno)s : %(msg)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt, "%b %d,%Y %H:%M:%S"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = __get_logger(f"plogger_{os_path.basename(__file__)}", logging.DEBUG)


def set_verbosity(level):
    global logger
    logger.setLevel(level)


def get_logger(name: str = "", level=logging.DEBUG) -> logging.Logger:
    global logger
    if len(name) == 0:
        logger.error("name cannot be empty")
    mLogger = __get_logger(name, level)
    return mLogger


if __name__ == "__main__":
    logger1 = get_logger("test",logging.ERROR)
    logger1.info("logger1")
    logger2 = get_logger("")
