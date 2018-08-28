
import logging
import sys
from unittest import TestCase
from unittest.mock import call

from applicationinsights import TelemetryClient
import pytest
from freezegun import freeze_time

from logger.config import config_loggers


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
                    '_lineno': 51,
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
