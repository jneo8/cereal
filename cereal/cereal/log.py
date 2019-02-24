"""Logger."""
import os
from distutils.util import strtobool
from colorlog import ColoredFormatter
from django.utils.log import DEFAULT_LOGGING


LOGLEVEL = os.environ.get("LOGLEVEL", 'debug').upper()
COLORLOG = os.environ.get("COLORLOG", True)

# Define console formatter
CONSOLE_FORMATTER = "console"

if strtobool(str(COLORLOG)):
    CONSOLE_FORMATTER = "color_console"


logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': str(
                '%(levelname)-8s '
                '%(asctime)s '
                '%(pathname)s %(funcName)s:%(lineno)s %(message)s',
            )
        },
        'color_console': {
            '()': 'colorlog.ColoredFormatter',
            'format': str(
                '%(log_color)s%(levelname)-8s%(reset)s '
                '%(yellow)s%(asctime)s %(green)s%(pathname)s '
                '%(green)s%(funcName)s:%(purple)s%(lineno)s '
                '%(blue)s%(message)s',
            ),
            'log_colors': {
                'DEBUG': 'bold_blue',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red',
            },
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': CONSOLE_FORMATTER,
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',  # noqa
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        '': {
            'handlers': ['sentry', 'console'],
            'level': "WARNING",
            'propagate': False,
        },
        # Don't send this module's logs to Sentry
        'noisy_module': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        'django': {
            'handlers': ['console'],
            'level': "INFO",
            'propagate': False,
        },
    },
}

