
import logging
from numbers import Number

from applicationinsights import TelemetryClient


class ApplicationInsightsHandler(logging.Handler):

    _name = 'application_insights'

    def __init__(
            self,
            app_insights_key,
            app_insights_app_id,
            app_insights_app_version,
            app_insights_device_id,
            app_insights_app_operation_name,
            correlation_id):

        super(ApplicationInsightsHandler, self).__init__()
        self.client = TelemetryClient(app_insights_key)
        self.app_insights_app_id = app_insights_app_id
        self.app_insights_app_version = app_insights_app_version
        self.app_insights_device_id = app_insights_device_id
        self.app_insights_app_operation_name = app_insights_app_operation_name
        self.correlation_id = correlation_id

    def emit(self, record):

        event = record.message
        measurements = {}
        properties = {
            '_name': record.name,
            '_created': record.created,
            '_func_name': record.funcName,
            '_file_name': record.filename,
            '_level_name': record.levelname,
            '_lineno': record.lineno,
        }

        self.client.context.operation.id = self.correlation_id
        self.client.context.application.id = self.app_insights_app_id
        self.client.context.application.ver = self.app_insights_app_version
        self.client.context.device.id = self.app_insights_device_id
        self.client.context.operation.name = (
            self.app_insights_app_operation_name)

        try:
            for k, v in record.args.items():
                if isinstance(v, Number):
                    measurements[k] = v

                else:
                    properties[k] = v

        except AttributeError:
            pass

        if record.exc_info:
            self.client.track_exception(
                *record.exc_info, properties, measurements)

        else:
            self.client.track_event(event, properties, measurements)

        self.client.flush()
