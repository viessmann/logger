
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self, log_record, record, message_dict):
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)

        # -- sometimes `args` is a tuple of values therefore the `update`
        # -- would fail
        try:
            log_record.update(record.args)

        except (TypeError, ValueError):
            pass
