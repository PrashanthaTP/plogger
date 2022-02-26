from collections import namedtuple
import logging
from os import path as os_path

logging.basicConfig(format="[%(levelname)s]  %(name)s | %(lineno)s : %(msg)s")


curr_dir = os_path.dirname(os_path.abspath(__file__))
settings_json = os_path.join(curr_dir, "log_settings.json")

Colors = namedtuple("Colors", ["fg", "bg", "style"])
LogLevels = namedtuple("LogLevels", ["debug", "info", "warning", "error"])
levels = LogLevels(logging.debug, logging.info,
                   logging.info, logging.error)


class CustomFormatter(logging.Formatter):
    """
    references : 
        - https://www.ing.iac.es//~docs/external/bash/abs-guide/colorizing.html#:~:text=the%20simplest%2c%20and%20perhaps%20most,%5b0%22%20switches%20it%20off.
        - https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    """
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
    default_fmt = "[%(levelname)s]  %(name)s | %(lineno)s : %(msg)s"
    default_fmts = LogLevels(default_fmt, default_fmt,
                             default_fmt, default_fmt)
    default_level_styles = LogLevels(
        Colors(green.fg, "", ""),
        Colors(cyan.fg, "", ""),
        Colors(red.fg, "", ""),
        Colors(red.fg, "", ""),
    )

    def escape(self, code):
        return f"\033[{code}m"

    def full_color_code(self, fmt, color: Colors):
        fg, bg, style = color.fg, color.bg, color.style
        if fg != "":
            fg = f"{fg};"
        else:
            fg = f"{CustomFormatter.white};"
        if bg == "":
            fg = fg.strip(";")
        if style != "":
            style = f"{style};"

        first_chunk = self.escape(f"{style}{fg}{bg}")
        last_chunk = self.escape(CustomFormatter.reset)
        return f"{first_chunk}{fmt}{last_chunk}"

    def __init__(self, fmts: LogLevels = None, level_styles: LogLevels = None):
        self.settings = level_styles or CustomFormatter.default_level_styles
        fmts = fmts or CustomFormatter.default_fmts
        self.formatters = {
            logging.DEBUG: logging.Formatter(self.full_color_code(
                fmts.debug, self.settings.debug)),
            logging.INFO: logging.Formatter(self.full_color_code(
                fmts.info, self.settings.info)),
            logging.WARNING: logging.Formatter(self.full_color_code(
                fmts.warning, self.settings.warning)),
            logging.ERROR: logging.Formatter(self.full_color_code(
                fmts.error, self.settings.error))
        }

    def format(self, record):
        return self.formatters.get(record.levelno, logging.Formatter(CustomFormatter.default_fmt)).format(record)


def read_settings():
    import json
    settings = {}
    with open(settings_json, 'r') as file:
        settings = json.load(file)
    return settings


def __get_logger(name: str, level=logging.debug) -> logging.Logger:
    fmt = "[%(levelname)s] %(name)s | %(lineno)s : %(msg)s"
    logger = logging.getLogger(name)

    if logger.hasHandlers() and len(logger.handlers) > 0:
        # then logger was already created with handlers
        # so we return the same instance of logger
        print(logger.handlers)
        logger.warning("%(name)s logger already exists!" % {"name": name})
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler()
    #handler.setFormatter(logging.Formatter(fmt, "%b %d,%Y %H:%M:%S"))
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger


mlogger = None


def init():
    global mlogger
    if mlogger is None:
        mlogger = __get_logger(f"plogger_{os_path.basename(__file__)}",
                               logging.DEBUG)


def require_init(fun):
    def wrapper(*args, **kwargs):
        init()
        return fun(*args, **kwargs)
    return wrapper


@require_init
def get_global_logger():
    global mlogger
    return mlogger


@require_init
def set_verbosity(level):
    global mlogger
    mlogger.setLevel(level)


@require_init
def get_logger(name: str = "", level=logging.DEBUG) -> logging.Logger:
    global mlogger
    if len(name) == 0:
        mlogger.error("name cannot be empty")
    new_logger = __get_logger(name, level)
    return new_logger


if __name__ == "__main__":
    print("Main........")
    CustomFormatter()
    logger1 = get_logger("aytala", logging.DEBUG)
    logger1.info("logger1")
    logger2 = get_logger("test2")
    logger2.debug('print')
