from functools import wraps as wrap_function
from io import StringIO
from logging import getLogger
from logging.config import dictConfig
from os import getcwd
from os.path import join as join_path

import click

from docker_dev_utils.exceptions import DockerDevUtilsException


_CURRENT_WORKDIR = getcwd()


_ERROR_LOG_FILE_NAME = 'docker-dev-utils.log'
_ERROR_LOG_FILE_PATH = join_path(_CURRENT_WORKDIR, _ERROR_LOG_FILE_NAME)
_ERROR_BUFFER_FILE = StringIO()


_BASE_LOGGING_CONFIG = {
    'version': 1,
    'root': {
        'handlers': ['errors'],
    },
    'handlers': {
        'errors': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
}


def _configure_logging():
    logging_config = _BASE_LOGGING_CONFIG.copy()
    logging_config['handlers']['errors']['stream'] = _ERROR_BUFFER_FILE
    dictConfig(logging_config)


def _write_command_errors_to_debug_file(command_function_original):
    @wrap_function(command_function_original)
    def command_function_wrapped(*args, **kwargs):
        _configure_logging()

        return_code = command_function_original(*args, **kwargs)

        was_function_successful = not return_code
        if not was_function_successful:
            _ERROR_BUFFER_FILE.seek(0)
            with open(_ERROR_LOG_FILE_PATH, 'w') as error_log_file:
                error_log_file.write(_ERROR_BUFFER_FILE.read())
            click.echo(
                'Debugging info written to {!r}'.format(_ERROR_LOG_FILE_PATH),
                err=True,
            )

        return return_code
    return command_function_wrapped


def log_command_errors(command_function_original):
    @wrap_function(command_function_original)
    @_write_command_errors_to_debug_file
    def command_function_wrapped(*arg, **kwargs):
        return_code = 1
        try:
            return_code = command_function_original(*arg, **kwargs)
        except Exception as exc:
            is_exception_supported = isinstance(exc, DockerDevUtilsException)
            message = exc if is_exception_supported else 'Unexpected error'

            click.echo(message, err=True)

            logger = getLogger(__name__)
            logger.exception(message)

        return return_code
    return command_function_wrapped
