import sys
import logging

from .logger import *

LOGGERS_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(levelname)s]: %(message)s'
        }
    },
    'filters': {
        'important_only': {
            '()': 'utils.logger.LevelFilter',
            'levels': [logging.NOTE, logging.CRITICAL]
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
            'stream': sys.stdout
        },
        'errors_file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': '',
            'level': logging.NOTE, # logging.NOTE = 25
        },
        'common_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': logging.INFO,
            'filename': '',
            'maxBytes': 1024*1024*5,
            'backupCount': 1
        },
        'debug_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
            'filename': '',
            'maxBytes': 1024*1024*2,
            'backupCount': 1
        },
        'main_file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filters': ['important_only'],
            'level': logging.NOTE,
            'filename': '',
        },
    },
    'loggers': {
        'template': {
            'handlers': ['console', 'errors_file', 'common_file', 'main_file'],
            'level': logging.DEBUG
        },
    }
}