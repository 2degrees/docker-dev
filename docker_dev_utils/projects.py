from os.path import join as join_path
from subprocess import check_output as run_command


def uninstall_project(project_path, project_name):
    # TODO: Handle errors
    docker_compose_project_file_path = \
        join_path(project_path, 'docker-compose.yml')
    run_command(
        [
            'docker-compose',
            '--file={}'.format(docker_compose_project_file_path),
            'down',
            '--rmi=all',
            '--volumes',
        ],
        env={'COMPOSE_PROJECT_NAME': project_name},
    )
