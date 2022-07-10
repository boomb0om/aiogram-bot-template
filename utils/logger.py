import logging
from logging.handlers import RotatingFileHandler
import sys
import os
from logging import Filter, LogRecord
import logging.config

# add new log level
NOTE_LEVEL_NUM = 25
logging.addLevelName(NOTE_LEVEL_NUM, "NOTE")
def notev(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    self._log(NOTE_LEVEL_NUM, message, args, **kws) 
logging.Logger.note = notev
logging.NOTE = NOTE_LEVEL_NUM

class LevelFilter(Filter):
    def __init__(self, levels):
        super().__init__()
        self.levels = levels

    def filter(self, record: LogRecord) -> int:
        passed = record.levelno in self.levels
        return passed


from .logger_config import LOGGERS_CONFIG

def setup_logger(bot_name, logging_dir='logs'):
    logfile_errors = os.path.join(logging_dir, f'errors_{bot_name}.log')
    logfile_info = os.path.join(logging_dir, f'info_{bot_name}.log')
    logfile_debug = os.path.join(logging_dir, f'debug_{bot_name}.log')
    logfile_main = os.path.join(logging_dir, f'main_{bot_name}.log')

    os.makedirs(logging_dir, exist_ok=True)
    
    LOGGERS_CONFIG['handlers']['errors_file']['filename'] = logfile_errors
    LOGGERS_CONFIG['handlers']['common_file']['filename'] = logfile_info
    LOGGERS_CONFIG['handlers']['debug_file']['filename'] = logfile_debug
    LOGGERS_CONFIG['handlers']['main_file']['filename'] = logfile_main
    
    logger_name = f'logger_{bot_name}'
    LOGGERS_CONFIG['loggers'][logger_name] = {
        'handlers': ['debug_file', 'errors_file', 'common_file', 'main_file', 'console'],
        'level': logging.DEBUG
    }
    
    logging.config.dictConfig(LOGGERS_CONFIG)
    logger = logging.getLogger(logger_name)
    logger.note('Logger initialized')
    return logger