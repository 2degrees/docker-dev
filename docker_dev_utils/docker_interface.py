from docker_dev_utils.subprocess import run_command


def run_docker_compose_subcommand(
    subcommand_name,
    subcommand_args,
    docker_compose_file_path,
    project_name
):
    project_file_arg = '--file={}'.format(docker_compose_file_path)
    command_args = [project_file_arg, subcommand_name] + subcommand_args
    command_environ = {'COMPOSE_PROJECT_NAME': project_name}
    output = run_command('docker-compose', command_args, command_environ)
    return output
