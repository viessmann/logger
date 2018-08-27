
from unittest import TestCase
from unittest.mock import Mock

from logger.formatters import JsonFormatter


class JsonFormatterTestCase(TestCase):

    def test_add_field(self):

        record = Mock(args={'hi': 'all'})
        message_dict = {'message': 'here'}
        log_record = {'hello': 'there'}

        JsonFormatter().add_fields(log_record, record, message_dict)

        assert log_record == {
            'hello': 'there',
            'message': 'here',
            'hi': 'all',
            'method_calls': [],
        }
