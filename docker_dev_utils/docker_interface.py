from os import environ
from os.path import isfile as is_file
from os.path import join as join_path
from subprocess import CalledProcessError
from subprocess import check_call as run_command
from tempfile import TemporaryFile

from docker_dev_utils.exceptions import ConfigurationError, SubprocessError, \
    MissingCommandError


def run_docker_compose_subcommand(
    subcommand_name,
    subcommand_args,
    project_path,
    project_name
):
    project_file_path = join_path(project_path, 'docker-compose.yml')
    if not is_file(project_file_path):
        raise ConfigurationError(
            'No such Docker Compose file {!r}'.format(project_file_path),
        )

    project_file_arg = '--file={}'.format(project_file_path)
    command_args = [project_file_arg, subcommand_name] + subcommand_args
    command_environ = {'COMPOSE_PROJECT_NAME': project_name}
    _run_command('docker-compose', command_args, command_environ)


def _run_command(command_name, command_args, additional_environ):
    command_parts = [command_name] + command_args
    command_environ = dict(additional_environ, PATH=environ['PATH'])
    command_stderr = TemporaryFile()
    try:
        run_command(command_parts, env=command_environ, stderr=command_stderr)
    except CalledProcessError as exc:
        command_stderr.seek(0)
        raise SubprocessError(
            command_parts,
            exc.returncode,
            command_stderr.read(),
        )
    except FileNotFoundError:
        raise MissingCommandError(command_name)
