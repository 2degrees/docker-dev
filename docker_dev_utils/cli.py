from os import getcwd
from os.path import basename

import click

from docker_dev_utils.exceptions import ConfigurationError
from docker_dev_utils._logging import handle_callback_exception
from docker_dev_utils.projects import uninstall_project, install_project
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
@click.pass_context
@handle_callback_exception
def main(context, project_path, project_name):
    # TODO: Should we require the path to docker-compose.yml instead and derive the project_path from it?
    # TODO: Make the `project_path` absolute
    context.obj = {'project_path': project_path, 'project_name': project_name}


@main.command()
@click.pass_obj
@handle_callback_exception
def clean(obj):
    uninstall_project(obj['project_path'], obj['project_name'])
