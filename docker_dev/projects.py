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
from os.path import dirname, basename
from shutil import rmtree

from docker_dev.docker_interface import run_docker_compose_subcommand, \
    get_docker_compose_config, run_docker_subcommand
from docker_dev.exceptions import VCSError, PluginError, SubprocessError
from docker_dev.plugins import get_objects_in_entry_point_group


_CONTAINER_TEST_REPORTS_PATH = "/tmp/test-reports"


def install_project(docker_compose_file_path, project_name):
    _run_host_pre_build_hooks(docker_compose_file_path, project_name)

    run_docker_compose_subcommand(
        'build',
        ['--pull'],
        docker_compose_file_path,
        project_name,
    )


def _run_host_pre_build_hooks(docker_compose_file_path, project_name):
    hooks = get_objects_in_entry_point_group('pre_build_hooks').items()
    for hook_name, hook in hooks:
        try:
            hook(docker_compose_file_path, project_name)
        except Exception as exc:
            raise PluginError(hook_name) from exc


def run_project(docker_compose_file_path, project_name):
    run_docker_compose_subcommand(
        'up',
        ['--force-recreate', '--abort-on-container-exit'],
        docker_compose_file_path,
        project_name,
    )


def test_project(docker_compose_file_path, project_name):
    test_service_names = \
        _get_test_service_names(docker_compose_file_path, project_name)
    for service_name in test_service_names:
        _run_test_service(docker_compose_file_path, project_name, service_name)


def _get_test_service_names(docker_compose_file_path, project_name):
    docker_compose_config = \
        get_docker_compose_config(docker_compose_file_path, project_name)
    service_names = docker_compose_config['services'].keys()
    test_service_names = [n for n in service_names if n.startswith('test')]
    return test_service_names


def _run_test_service(docker_compose_file_path, project_name, service_name):
    try:
        run_docker_compose_subcommand(
            'run',
            ['-T', '--name', project_name, service_name],
            docker_compose_file_path,
            project_name,
        )
        _export_test_results(project_name, service_name)
    finally:
        try:
            run_docker_subcommand('rm', ['--volumes', '--force', project_name])
        except SubprocessError:
            pass


def _export_test_results(project_name, service_name):
    rmtree(service_name, ignore_errors=True)
    run_docker_subcommand(
        'cp',
        [
            '{}:{}'.format(project_name, _CONTAINER_TEST_REPORTS_PATH),
            service_name,
        ],
    )


def uninstall_project(docker_compose_file_path, project_name):
    run_docker_compose_subcommand(
        'down',
        ['--rmi=all', '--volumes'],
        docker_compose_file_path,
        project_name,
    )


def get_default_project_name(docker_compose_file_path):
    project_path = dirname(docker_compose_file_path)
    project_name_generated = _generate_project_name_from_path(project_path)
    project_name = project_name_generated or basename(project_path)
    return project_name


def _generate_project_name_from_path(path):
    project_name_generators = get_objects_in_entry_point_group(
        'project_name_generator',
    )
    project_name = None
    for project_name_generator in project_name_generators.values():
        try:
            project_name = project_name_generator(path)
        except VCSError:
            continue
        else:
            break
    return project_name
