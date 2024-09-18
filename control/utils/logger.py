
import threading
from control.config import settings
from control.filesystem.fs import FileSystem

class LogLevel:
    NO_LOGS = (-1, 'NO_LOGS')

    SUCCESS  = (0, 'SUCCESS')
    CRITICAL = (0, 'CRITICAL')
    ERROR    = (1, 'ERROR')
    WARNING  = (2, 'WARNING')
    INFO     = (3, 'INFO')
    DEBUG    = (4, 'DEBUG')

class Logger:
    def __init__(self, path: str) -> None:
        self.file = FileSystem.open_unique(path, "w")

        self.lock = threading.Lock()

    def close(self):
        self.file.close()
        self.file = None

    def __log (self, level: LogLevel, message: str):
        tier, name = level

        if tier > settings.MAX_LOG_LEVEL: return

        if self.file is not None:
            self.file.write(message)
            self.file.flush()
    def __log_prepare (self, level: LogLevel, *args):
        message = f"[{level[1]}] {' '.join(list(map(str, args)))}\n"

        self.__log(level, message)

    def success (self, *args):
        self.__log_prepare(LogLevel.SUCCESS, *args)
    def critical (self, *args):
        self.__log_prepare(LogLevel.CRITICAL, *args)
    def error (self, *args):
        self.__log_prepare(LogLevel.ERROR, *args)
    def warning (self, *args):
        self.__log_prepare(LogLevel.WARNING, *args)
    def info (self, *args):
        self.__log_prepare(LogLevel.INFO, *args)
    def debug (self, *args):
        self.__log_prepare(LogLevel.DEBUG, *args)
