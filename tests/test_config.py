
import json
import logging
import sys
from unittest import TestCase
from unittest.mock import call

from applicationinsights import TelemetryClient
import pytest
from freezegun import freeze_time

from logger.config import (
    config_loggers,
    with_logger,
    LoggingNotConfiguredError,
)


@freeze_time('2012-01-14 03:21:34')
class ConfigLoggersTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def test_config_loggers__local(self):

        config_loggers()

        write = self.mocker.patch.object(sys.stdout, 'write')
        track_event = self.mocker.patch.object(TelemetryClient, 'track_event')

        logger = logging.getLogger()
        logger.info('SOME_EVENT', {'hi': 'there'})

        assert write.call_args_list == [
            call('{"message": "SOME_EVENT", "hi": "there"}'),
            call('\n'),
        ]
        assert track_event.call_args_list == []

    def test_config_loggers__remote(self):

        config_loggers(
            app_insights_key='key',
            app_insights_app_id='avro',
            app_version='0.0.7',
            app_name='app',
            correlation_id='189',
            execution_env_name='aws')

        write = self.mocker.patch.object(sys.stdout, 'write')
        track_event = self.mocker.patch.object(TelemetryClient, 'track_event')

        logger = logging.getLogger()
        logger.info('SOME_EVENT', {'a': 11})

        assert write.call_args_list == [
            call('{"message": "SOME_EVENT", "a": 11}'),
            call('\n'),
        ]
        assert track_event.call_args_list == [
            call(
                'SOME_EVENT',
                {
                    '_file_name': 'test_config.py',
                    '_lineno': 56,
                    '_name': 'root',
                    '_func_name': 'test_config_loggers__remote',
                    '_created': 1326511294.0,
                    '_level_name': 'INFO',
                },
                {
                    'a': 11,
                },
            ),
        ]


@freeze_time('2012-01-14 03:21:34')
class WithLoggerTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def test_log_to_application_insights(self):

        config_loggers(
            app_insights_key='key',
            app_insights_app_id='avro',
            app_version='0.0.7',
            app_name='app',
            correlation_id='189',
            execution_env_name='aws')

        track_event = self.mocker.patch.object(TelemetryClient, 'track_event')

        @with_logger
        def fn(x, logger):
            logger.info('SOME_EVENT', {'a': 11})

            return 11

        assert fn(12) == 11
        assert track_event.call_args_list == [
            call(
                'SOME_EVENT',
                {
                    '_file_name': 'test_config.py',
                    '_lineno': 101,
                    '_name': 'root',
                    '_func_name': 'fn',
                    '_created': 1326511294.0,
                    '_level_name': 'INFO',
                },
                {
                    'a': 11,
                },
            ),
        ]

    def test_when_decorated_function_raises_exception(self):

        class SomeError(Exception):
            pass

        config_loggers()

        write = self.mocker.patch.object(sys.stdout, 'write')

        @with_logger
        def fn(x, logger):
            raise SomeError

        try:
            fn(12)

        except SomeError:
            assert write.call_count == 2
            args = json.loads(write.call_args_list[0][0][0])
            assert args['message'] == 'UNHANDLED_EXCEPTION_CAUGHT'
            assert args['exc_info'].startswith('Traceback')

        else:
            raise AssertionError('should raise error')

    def test_when_configuration_was_not_set(self):

        self.mocker.patch('logger.config.LOG_CONFIG', None)

        @with_logger
        def fn(x, logger):
            return x

        try:
            fn(12)

        except LoggingNotConfiguredError:
            pass

        else:
            raise AssertionError('should raise error')
