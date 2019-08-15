from colorama import init
from enum import Enum

init()


class ANSIColor(Enum):

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 0


class DebugColorLevel(Enum):

    WARNING         = ANSIColor.YELLOW.value
    INFO            = ANSIColor.WHITE.value
    DEBUG           = ANSIColor.CYAN.value
    CRITICAL        = ANSIColor.YELLOW.value
    ERROR           = ANSIColor.RED.value
    TEST            = ANSIColor.MAGENTA.value
    SUCCESS         = ANSIColor.GREEN.value
    NOTIFICATION    = ANSIColor.BLUE.value


class Logger(object):

    LABEL = ''

    @staticmethod
    def _colorize_message(color: int, msg: str):
        msg_format = u'\u001b[1m[{label}]: \u001b[1;{msg_color_code}m{msg}\u001b[{reset_color}m'
        return msg_format.format(label=Logger.LABEL,
                msg_color_code=color,
                msg=msg,
                reset_color=ANSIColor.RESET.value)

    @staticmethod
    def warning(msg: str):
        Logger.LABEL = 'WARNING'
        print(Logger._colorize_message(DebugColorLevel.WARNING.value, msg))

    @staticmethod
    def info(msg: str):
        Logger.LABEL = 'INFO'
        print(Logger._colorize_message(DebugColorLevel.INFO.value, msg))

    @staticmethod
    def debug(msg: str):
        Logger.LABEL = 'DEBUG'
        print(Logger._colorize_message(DebugColorLevel.DEBUG.value, msg))

    @staticmethod
    def critical(msg: str):
        Logger.LABEL = 'CRITICAL'
        print(Logger._colorize_message(DebugColorLevel.CRITICAL.value, msg))

    @staticmethod
    def error(msg: str):
        Logger.LABEL = 'ERROR'
        print(Logger._colorize_message(DebugColorLevel.ERROR.value, msg))

    @staticmethod
    def test(msg: str):
        Logger.LABEL = 'TEST'
        print(Logger._colorize_message(DebugColorLevel.TEST.value, msg))

    @staticmethod
    def success(msg: str):
        Logger.LABEL = 'SUCCESS'
        print(Logger._colorize_message(DebugColorLevel.SUCCESS.value, msg))

    @staticmethod
    def notify(msg: str):
        Logger.LABEL = 'NOTIFICATION'
        print(Logger._colorize_message(DebugColorLevel.NOTIFICATION.value, msg))
