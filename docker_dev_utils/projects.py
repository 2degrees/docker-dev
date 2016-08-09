from docker_dev_utils.docker_interface import run_docker_compose_subcommand


def uninstall_project(project_path, project_name):
    run_docker_compose_subcommand(
        'down',
        ['--rmi=all', '--volumes'],
        project_path,
        project_name,
    )
