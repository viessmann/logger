
from unittest import TestCase
from unittest.mock import Mock

from applicationinsights import TelemetryClient
import pytest

from logger.handlers import ApplicationInsightsHandler


class ApplicationInsightsHandlerTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def test_emit(self):

        self.mocker.patch.object(TelemetryClient, 'track_event')
        a = ApplicationInsightsHandler(
            app_insights_key='some.key',
            app_insights_app_id='job',
            app_insights_app_version='1.0.1',
            app_insights_device_id='databricks',
            app_insights_app_operation_name='super job',
            correlation_id='123')

        a.emit(
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
