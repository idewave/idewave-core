from colorama import Fore, Back, Style
from enum import Enum


class DebugColorLevel(Enum):

    INFO            = Back.WHITE + Fore.BLACK
    WARNING         = Fore.YELLOW
    CRITICAL        = Fore.YELLOW + Style.BRIGHT
    ERROR           = Fore.RED + Style.BRIGHT
    SUCCESS         = Fore.GREEN + Style.BRIGHT
    DEBUG           = Fore.CYAN + Style.BRIGHT
    TEST            = Fore.MAGENTA + Style.BRIGHT
    NOTIFICATION    = Fore.BLUE + Style.BRIGHT


class Logger(object):

    LABEL = ''

    @staticmethod
    def _colorize_message(color: str, msg: str):
        msg_format =  color + '{label}{reset_color}  {msg}'
        return msg_format.format(label=Logger.LABEL,
                msg_color_code=color,
                msg=msg,
                reset_color=Style.RESET_ALL)

    @staticmethod
    def debug(msg: str):
        Logger.LABEL = '[DEBUG]'
        print(Logger._colorize_message(DebugColorLevel.DEBUG.value, msg))

    @staticmethod
    def warning(msg: str):
        Logger.LABEL = '[WARNING]'
        print(Logger._colorize_message(DebugColorLevel.WARNING.value, msg))

    @staticmethod
    def error(msg: str):
        Logger.LABEL = '[ERROR]'
        print(Logger._colorize_message(DebugColorLevel.ERROR.value, msg))

    @staticmethod
    def info(msg: str):
        Logger.LABEL = '[INFO]'
        print(Logger._colorize_message(DebugColorLevel.INFO.value, msg))

    @staticmethod
    def test(msg: str):
        Logger.LABEL = '[TEST]'
        print(Logger._colorize_message(DebugColorLevel.TEST.value, msg))

    @staticmethod
    def success(msg: str):
        Logger.LABEL = '[SUCCESS]'
        print(Logger._colorize_message(DebugColorLevel.SUCCESS.value, msg))

    @staticmethod
    def notify(msg: str):
        Logger.LABEL = '[NOTIFICATION]'
        print(Logger._colorize_message(DebugColorLevel.NOTIFICATION.value, msg))
