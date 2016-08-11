from functools import wraps as wrap_function
from logging import getLogger
from logging.config import dictConfig as configure_logging
from tempfile import NamedTemporaryFile

import click
from click.globals import get_current_context

from docker_dev_utils.exceptions import DockerDevUtilsException


_ERROR_LOG_FILE = \
    NamedTemporaryFile(prefix='docker-dev-utils-', suffix='.log', delete=False)
_ERROR_LOG_FILE_PATH = _ERROR_LOG_FILE.name


_LOGGING_CONFIG = {
    'version': 1,
    'root': {
        'handlers': ['errors'],
    },
    'formatters': {
        'main': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'errors': {
            'class': 'logging.FileHandler',
            'filename': _ERROR_LOG_FILE_PATH,
            'level': 'INFO',
            'formatter': 'main',
        },
    },
}


def _log_callback_exception(exc):
    logger = getLogger(__name__)
    logger.exception('', exc_info=exc)

    click.echo(
        'Debugging info written to {!r}'.format(_ERROR_LOG_FILE_PATH),
        err=True,
    )


def _fail(exc):
    is_exception_supported = isinstance(exc, DockerDevUtilsException)
    message = exc if is_exception_supported else 'Unexpected error'
    click.echo('Error: ' + str(message), err=True)

    context = get_current_context()
    context.exit(1)


def handle_callback_exception(callback_original):
    @wrap_function(callback_original)
    def callback_wrapped(*args, **kwargs):
        configure_logging(_LOGGING_CONFIG)
        try:
            return callback_original(*args, **kwargs)
        except Exception as exc:
            _log_callback_exception(exc)
            _fail(exc)

    return callback_wrapped
