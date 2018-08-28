
from logging import config


def config_loggers(
        app_insights_key=None,
        app_insights_app_id=None,
        app_version=None,
        app_name=None,
        correlation_id=None,
        execution_env_name=None):

    if app_insights_key:
        config.dictConfig({
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
        })

    else:
        config.dictConfig({
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
        })
