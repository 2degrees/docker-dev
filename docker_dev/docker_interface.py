##############################################################################
#
# Copyright (c) 2016, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of django-pastedeploy-settings
# <https://github.com/2degrees/django-pastedeploy-settings>, which is subject
# to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################
from docker_dev.subprocess import run_command
from yaml import safe_load as yaml_deserialize


def run_docker_compose_subcommand(
    subcommand_name,
    subcommand_args,
    docker_compose_file_path,
    project_name,
    return_stdout=True,
):
    project_file_arg = '--file={}'.format(docker_compose_file_path)
    command_args = [project_file_arg, subcommand_name] + subcommand_args
    command_environ = {'COMPOSE_PROJECT_NAME': project_name}
    output = run_command(
        'docker-compose',
        command_args,
        command_environ,
        return_stdout,
    )
    return output


def get_docker_compose_config(docker_compose_file_path, project_name):
    docker_compose_config_yaml = run_docker_compose_subcommand(
        'config',
        [],
        docker_compose_file_path,
        project_name,
    )
    docker_compose_config = yaml_deserialize(docker_compose_config_yaml)
    return docker_compose_config


def run_docker_subcommand(subcommand_name, subcommand_args):
    command_args = [subcommand_name] + subcommand_args
    output = run_command('docker', command_args)
    return output
