from functools import wraps as wrap_function
from os import getcwd
from os.path import basename

import click

from docker_dev_utils.exceptions import ConfigurationError
from docker_dev_utils.exceptions import DockerDevUtilsException
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


def _print_expected_error(function_original):
    @wrap_function(function_original)
    def function_wrapped(*arg, **kwargs):
        try:
            return_code = function_original(*arg, **kwargs)
        except DockerDevUtilsException as exc:
            click.echo(exc, err=True)
            return_code = 1
        return return_code
    return function_wrapped


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
@_print_expected_error
def main(context, project_path, project_name):
    # TODO: Should we require the path to docker-compose.yml instead and derive the project_path from it?
    # TODO: Make the `project_path` absolute
    context.obj = {'project_path': project_path, 'project_name': project_name}


@main.command()
@click.pass_obj
@_print_expected_error
def clean(obj):
    uninstall_project(obj['project_path'], obj['project_name'])
