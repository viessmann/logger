
import logging
from logging import config


LOG_CONFIG = None


class LoggingNotConfiguredError(Exception):
    """
    Error to be raised whenever one wants to use helper functions that are
    assuming that logging was already configured when in fact it wasn't.
    """

    pass


def with_logger(fn):

    def inner(*args):
        if not LOG_CONFIG:
            raise LoggingNotConfiguredError()

        config.dictConfig(LOG_CONFIG)
        logger = logging.getLogger()

        try:
            return fn(*args, logger)

        except Exception as e:
            logger.error('UNHANDLED_EXCEPTION_CAUGHT', exc_info=True)

            raise e

    return inner


def config_loggers(
        app_insights_key=None,
        app_insights_app_id=None,
        app_version=None,
        app_name=None,
        correlation_id=None,
        execution_env_name=None):

    # -- declare `LOG_CONFIG` to overload the globally accessible value
    global LOG_CONFIG

    if app_insights_key:
        LOG_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'root': {
                'level': 'INFO',
                'handlers': ['console', 'application_insights'],
            },
            'formatters': {
                'json_formatter': {
                    'class': 'logger.formatters.JsonFormatter',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json_formatter',
                    'level': 'DEBUG',
                    'stream': 'ext://sys.stdout',
                },
                'application_insights': {
                    'class': 'logger.handlers.ApplicationInsightsHandler',
                    'formatter': 'json_formatter',
                    'level': 'INFO',
                    'correlation_id': correlation_id,
                    'app_insights_key': app_insights_key,
                    'app_insights_app_id': app_insights_app_id,
                    'app_insights_app_version': app_version,
                    'app_insights_device_id': execution_env_name,
                    'app_insights_app_operation_name': app_name,
                },
            },
            'loggers': {
                'root': {
                    'handlers': ['console', 'application_insights'],
                }
            }
        }

    else:
        LOG_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'root': {
                'level': 'INFO',
                'handlers': ['console'],
            },
            'formatters': {
                'json_formatter': {
                    'class': 'logger.formatters.JsonFormatter',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json_formatter',
                    'level': 'INFO',
                    'stream': 'ext://sys.stdout',
                },
            },
            'loggers': {
                'root': {
                    'handlers': ['console'],
                }
            }
        }

    config.dictConfig(LOG_CONFIG)
