from os.path import isfile as is_file
from os.path import join as join_path

from docker_dev_utils.exceptions import ConfigurationError
from docker_dev_utils.subprocess import run_command


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
    output = run_command('docker-compose', command_args, command_environ)
    return output
