from os import getcwd
from os.path import basename

import click

from docker_dev_utils.exceptions import ConfigurationError
from docker_dev_utils.projects import uninstall_project
from docker_dev_utils.vcs import get_repository_info_from_path


_CURRENT_WORKDIR = getcwd()
try:
    _CURRENT_PROJECT_INFO = get_repository_info_from_path(_CURRENT_WORKDIR)
except ConfigurationError:
    _DEFAULT_PROJECT_PATH = None
    _DEFAULT_PROJECT_NAME = None
else:
    _DEFAULT_PROJECT_PATH = _CURRENT_PROJECT_INFO.path
    _DEFAULT_PROJECT_NAME = '{}-{}'.format(
        basename(_DEFAULT_PROJECT_PATH),
        _CURRENT_PROJECT_INFO.branch_name,
    )


@click.group()
@click.option(
    '--project-path',
    default=_DEFAULT_PROJECT_PATH,
    show_default=True,
)
@click.option(
    '--project-name',
    default=_DEFAULT_PROJECT_NAME,
    show_default=True,
)
def main(project_path, project_name):
    # TODO: Should we require the path to docker-compose.yml instead and derive the project_path from it?
    # TODO: Make the `project_path` absolute
    pass


@main.command()
def clean():
    uninstall_project(project_path, project_name)
