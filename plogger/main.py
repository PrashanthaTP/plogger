from collections import namedtuple
import logging
from os import path as os_path

logging.basicConfig(format="[%(levelname)s]  %(name)s | %(lineno)s : %(msg)s")


CURR_DIR = os_path.dirname(os_path.abspath(__file__))
SETTINGS_JSON = os_path.join(CURR_DIR, "log_settings.json")

Colors = namedtuple("Colors", ["FG", "BG", "STYLE"])
LogLevels = namedtuple("LogLevels", ["DEBUG", "INFO", "WARNING", "ERROR"])
LEVELS = LogLevels(logging.DEBUG, logging.INFO,
                   logging.INFO, logging.ERROR)


class CustomFormatter(logging.Formatter):
    black = Colors(30, 40, "")
    red = Colors(31, 41, "")
    green = Colors(32, 42, "")
    yellow = Colors(33, 43, "")
    blue = Colors(34, 44, "")
    magenta = Colors(35, 45, "")
    cyan = Colors(36, 46, "")
    white = Colors(37, 47, "")
    reset = "0"
    bold = "1"

    def escape(self, code):
        return f"\033[{code}m"

    def full_color_code(self, fmt, colors: Colors):
        fg, bg, style = colors.FG, colors.BG, colors.STYLE
        first_chunk = self.escape(f"{style};{fg};{bg}")
        last_chunk = self.escape(CustomFormatter.escape)
        return f"{first_chunk}{fmt}{last_chunk}"

    def __init__(self, fmts: LogLevels, level_styles: LogLevels):
        self.settings = level_styles
        self.formatters = {
            logging.DEBUG: logging.Formatter(self.full_color_code(
                fmts.DEBUG, self.settings.DEBUG)),
            logging.INFO: logging.Formatter(self.full_color_code(
                fmts.INFO, self.settings.INFO)),
            logging.WARNING: logging.Formatter(self.full_color_code(
                fmts.WARNING, self.settings.WARNING)),
            logging.ERROR: logging.Formatter(self.full_color_code(
                fmts.ERROR, self.settings.ERROR))
        }

    def format(self, record):
        return self.formatters.get(record.levelno, logging.DEBUG)


def read_settings():
    import json
    settings = {}
    with open(SETTINGS_JSON, 'r') as file:
        settings = json.load(file)
    return settings


def __get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    fmt = "[%(levelname)s] %(name)s | %(lineno)s : %(msg)s"
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        # then logger was already created with handlers
        # so we return the same instance of logger
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt, "%b %d,%Y %H:%M:%S"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = None


def init():
    global logger
    if logger is None:
        logger = __get_logger(f"plogger_{os_path.basename(__file__)}",
                              logging.DEBUG)


def require_init(fun):
    def wrapper(*args, **kwargs):
        init()
        return fun(*args, **kwargs)
    return wrapper


@require_init
def set_verbosity(level):
    global logger
    logger.setLevel(level)


@require_init
def get_logger(name: str = "", level=logging.DEBUG) -> logging.Logger:
    global logger
    if len(name) == 0:
        logger.error("name cannot be empty")
    mLogger = __get_logger(name, level)
    return mLogger


if __name__ == "__main__":
    logger1 = get_logger("test", logging.ERROR)
    logger1.info("logger1")
    logger2 = get_logger("")
