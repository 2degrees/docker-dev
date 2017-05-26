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
from os.path import basename, relpath

from docker_dev.exceptions import VCSError, MissingCommandError, \
    SubprocessError
from docker_dev.subprocess import run_command


def get_project_name(project_path):
    _assert_git_executable_is_available()

    repo_path = _get_repo_path_from_path(project_path)
    if repo_path:
        repo_name = basename(repo_path)
        branch_name = _get_current_branch_name_in_path(project_path)
        project_name_parts = [repo_name, branch_name]

        project_path_relative = relpath(project_path, repo_path)
        if project_path_relative:
            project_name_parts.append(project_path_relative.replace('/', ''))

        project_name = '-'.join(project_name_parts)
    else:
        project_name = None
    return project_name


def _get_repo_path_from_path(path):
    try:
        repo_path = run_command(
            'git',
            ['rev-parse', '--show-toplevel'],
            cwd=path,
        )
    except SubprocessError:
        repo_path = None
    return repo_path


def _get_current_branch_name_in_path(path):
    branch_reference = run_command(
        'git',
        ['symbolic-ref', '-q', 'HEAD'],
        cwd=path,
    )
    branch_name = branch_reference.split('/')[-1]
    return branch_name


def _assert_git_executable_is_available():
    try:
        run_command('git', ['--version'])
    except MissingCommandError as exc:
        raise VCSError('Git is not installed') from exc
