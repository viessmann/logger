
from unittest import TestCase
from unittest.mock import call, Mock

import pytest

from logger.handlers import ApplicationInsightsHandler


class ApplicationInsightsHandlerTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):

        TelemetryClient = self.mocker.patch(  # noqa
            'logger.handlers.TelemetryClient')
        self.client = Mock()
        TelemetryClient.return_value = self.client

        self.handler = ApplicationInsightsHandler(
            app_insights_key='some.key',
            app_insights_app_id='job',
            app_insights_app_version='1.0.1',
            app_insights_device_id='databricks',
            app_insights_app_operation_name='super job',
            correlation_id='123')

    def test_emit__sets_context_data(self):

        handler = ApplicationInsightsHandler(
            app_insights_key='some.key',
            app_insights_app_id='job',
            app_insights_app_version='1.0.1',
            app_insights_device_id='databricks',
            app_insights_app_operation_name='super job',
            correlation_id='123')

        handler.emit(
            Mock(
                message='hello world',
                name='file',
                created='now',
                funcName='fn',
                filename='file',
                levelname='INFO',
                lineno=11,
                exc_info=None,
                args=(),
            ))

        assert self.client.context.operation.id == '123'
        assert self.client.context.application.id == 'job'
        assert self.client.context.application.ver == '1.0.1'
        assert self.client.context.device.id == 'databricks'
        assert self.client.context.operation.name == 'super job'

    def test_emit__track_event__without_args(self):

        record = Mock(
            message='hello world',
            created='now',
            funcName='fn',
            filename='file',
            levelname='INFO',
            lineno=11,
            exc_info=None,
            args=())

        self.handler.emit(record)

        assert self.client.track_event.call_args_list == [
            call(
                'hello world',
                {
                    '_created': 'now',
                    '_lineno': 11,
                    '_name': record.name,
                    '_level_name': 'INFO',
                    '_file_name': 'file',
                    '_func_name': 'fn',
                },
                {},
            ),
        ]

    def test_emit__track_event__with_args(self):

        record = Mock(
            message='hello world',
            created='now',
            funcName='fn',
            filename='file',
            levelname='INFO',
            lineno=11,
            exc_info=None,
            args={
                'value': 11,
                'datetime': 1902.32,
                'start': '2018-01-12',
            })

        self.handler.emit(record)

        assert self.client.track_event.call_args_list == [
            call(
                'hello world',
                {
                    '_created': 'now',
                    '_lineno': 11,
                    '_name': record.name,
                    '_level_name': 'INFO',
                    '_file_name': 'file',
                    '_func_name': 'fn',
                    # -- non-numerical values goes here
                    'start': '2018-01-12',
                },
                {
                    # -- numerical values goes here
                    'value': 11,
                    'datetime': 1902.32,
                },
            ),
        ]

    def test_emit__exception(self):

        record = Mock(
            message='hello world',
            created='now',
            funcName='fn',
            filename='file',
            levelname='INFO',
            lineno=11,
            exc_info=('exec', 'info'),
            args={
                'value': 189,
                'datetime': 210.01,
                'start': '2018-01-12',
            })

        self.handler.emit(record)

        assert self.client.track_event.call_count == 0
        assert self.client.track_exception.call_args_list == [
            call(
                'exec',
                'info',
                {
                    '_func_name': 'fn',
                    '_created': 'now',
                    '_name': record.name,
                    'start': '2018-01-12',
                    '_file_name': 'file',
                    '_lineno': 11,
                    '_level_name': 'INFO',
                },
                {
                    'value': 189,
                    'datetime': 210.01,
                },
            ),
        ]
