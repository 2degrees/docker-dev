from os.path import basename, abspath

import click

from docker_dev_utils._logging import handle_callback_exception
from docker_dev_utils.projects import uninstall_project, \
    get_project_name_refinement, install_project


def _convert_click_path_arg_to_absolute(ctx, param, value):
    return abspath(value)


def _calculate_default_project_name(ctx, param, value):
    if value:
        project_name = value
    else:
        project_path = ctx.params['project_path']
        project_name = basename(project_path)
        project_name_refinement = get_project_name_refinement(project_path)
        if project_name_refinement:
            project_name = '{}-{}'.format(project_name, project_name_refinement)
    return project_name


@click.group()
@click.option(
    '--project-path',
    default='.',
    show_default=True,
    callback=_convert_click_path_arg_to_absolute,
    is_eager=True,
)
@click.option('--project-name', callback=_calculate_default_project_name)
@handle_callback_exception
def main(project_path, project_name):
    # TODO: Should we require the path to docker-compose.yml instead and derive the project_path from it?
    pass


@main.command()
@click.pass_context
@handle_callback_exception
def build(context):
    main_args = context.parent.params
    install_project(main_args['project_path'], main_args['project_name'])


@main.command()
@click.pass_context
@handle_callback_exception
def clean(context):
    main_args = context.parent.params
    uninstall_project(main_args['project_path'], main_args['project_name'])
