##############################################################################
#
# Copyright (c) 2016-2017, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of docker-dev
# <https://github.com/2degrees/docker-dev>, which is subject
# to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

import click

from docker_dev._logging import handle_callback_exception
from docker_dev.docker_interface import run_docker_compose_subcommand
from docker_dev.exceptions import SubprocessError
from docker_dev.projects import uninstall_project, \
    get_default_project_name, install_project, run_project, test_project


def _calculate_default_project_name(ctx, param, value):
    if value:
        project_name = value
    else:
        docker_compose_file_path = ctx.params['docker_compose_file_path']
        project_name = get_default_project_name(docker_compose_file_path)
    return project_name


@click.group()
@click.option(
    '--docker-compose-file-path',
    default='docker-compose.yml',
    show_default=True,
    is_eager=True,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.option('--project-name', callback=_calculate_default_project_name)
@handle_callback_exception
def main(docker_compose_file_path, project_name):
    pass


@main.command()
@click.pass_context
@handle_callback_exception
def build(context):
    main_args = context.parent.params
    install_project(
        main_args['docker_compose_file_path'],
        main_args['project_name'],
    )


@main.command()
@click.pass_context
@handle_callback_exception
def up(context):
    main_args = context.parent.params
    run_project(
        main_args['docker_compose_file_path'],
        main_args['project_name'],
    )


@main.command()
@click.pass_context
@handle_callback_exception
@click.option('--force-build', is_flag=True)
@click.option('--cleanup', is_flag=True)
def test(context, force_build, cleanup):
    main_args = context.parent.params
    docker_compose_file_path = main_args['docker_compose_file_path']
    base_project_name = main_args['project_name']
    project_name = base_project_name + '-test'

    if force_build:
        try:
            uninstall_project(docker_compose_file_path, project_name)
        except SubprocessError:
            pass
        install_project(docker_compose_file_path, project_name)

    test_project(docker_compose_file_path, project_name)

    if cleanup:
        uninstall_project(docker_compose_file_path, project_name)


@main.command()
@click.pass_context
@handle_callback_exception
def down(context):
    main_args = context.parent.params
    uninstall_project(
        main_args['docker_compose_file_path'],
        main_args['project_name'],
    )


@main.command(context_settings={'ignore_unknown_options': True})
@click.pass_context
@handle_callback_exception
@click.argument('subcommand')
@click.argument('subcommand-args', type=click.UNPROCESSED, nargs=-1)
def dc(context, subcommand, subcommand_args):
    main_args = context.parent.params
    run_docker_compose_subcommand(
        subcommand,
        list(subcommand_args),
        main_args['docker_compose_file_path'],
        main_args['project_name'],
    )
