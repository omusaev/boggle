import importlib.util
import logging
import os

from logging import config as logging_config

# 1. default settings for all envs
from conf.defaults import *

logging.basicConfig(level='INFO')


APP_ENVIRONMENT_NAME = os.environ.get('APP_ENVIRONMENT_NAME', 'dev')
logging.info('Loading configuration for env: {}'.format(APP_ENVIRONMENT_NAME))

# 2. env settings
environment_settings_module = \
    '{}/envs/{}.py'.format(os.path.dirname(__file__), APP_ENVIRONMENT_NAME)
spec = importlib.util.spec_from_file_location(
    'env_settings', environment_settings_module)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for setting in filter(lambda k: not k.startswith('_'), dir(module)):
    locals()[setting] = getattr(module, setting)

# 3. overrides by ENV variables with prefix APP_
for key in filter(lambda k: k.startswith('APP_'), os.environ.keys()):
    setting = key.replace('APP_', '', 1)
    logging.info('Found a redefine for {} in env vars'.format(setting))
    value = os.environ.get(key)
    locals()[setting] = value

# 4. overrides by local settings
try:
    from settings_local import *
    logging.info('Found a settings_local file')
except ImportError:
    pass


'''
See https://docs.python.org/2/howto/logging.html#logging-flow for more details
If you don't want logs to be passed to parent loggers set propagate to False:

...
    'logger_name': {
        'propagate': False,
    }
...

'''
LOGGERS = {
    '': {
        'handlers': ['console'],
        'level': LOGGING_LEVEL,
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(name)s %(thread)d [%(asctime)s] %(filename)s:%(lineno)s %(message)s',
            'datefmt': '%d/%b/%Y:%H:%M:%S %z',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'datefmt': '%d/%b/%Y:%H:%M:%S %z',
            'fmt': '%(levelname)s %(name)s [%(asctime)s] %(pathname)s %(lineno)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
        }
    },
    'loggers': LOGGERS
}

logging_config.dictConfig(LOGGING)
