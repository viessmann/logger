
# Logger

Logger wrapper allowing one to stream logs to both `stdout` and Azure Application Insights.

It uses python's standard library logging capability to expose custom handlers and formatters for communication with Azure Application Insights.


## Usage

In order to use just before your first usage of the logger (where you call `logging.getLogger()`) make a call the following call:

```python
from logger.config import config_loggers

config_loggers(
    app_insights_key='<YOU.KEY>',
    app_insights_app_id='<APP.ID>',
    app_version='<APP.VERSION>',
    app_name='<APP.NAME>',
    correlation_id='<CORRELATION.ID>',
    execution_env_name='DataBricks'):

logger = logging.getLogger()

logger.info('SOMETHING_HAPPENED', {'start': 123})

```

Also if the configuration delivered with the `config_loggers` is not fulfilling all criteria one can use is a merely an inspiration and provide ones own customization.


## Logging / Format

The underlying formatter and handler is expecting the logs to be invoked in a particular format:

```python

logger('SOME_EVENT_NAME', {'here': 'extra data'})

```

for example:

```python

logger(
    'ARES_JOB_SUCCEEDED',
    {'count': 11, 'datetime': '2018-11-12T12:32:31'})

```

Where all numerical values will end up in the `measurements` part of Application Insights and all non-numerical will end up in the `properties` part.

Also the `properties` will be enriched by some meta information allowing one to understand the invocation context.
