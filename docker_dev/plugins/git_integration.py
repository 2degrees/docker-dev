from os.path import dirname

from docker_dev.exceptions import VCSError, MissingCommandError, \
    SubprocessError
from docker_dev.subprocess import run_command


def get_active_branch_name(docker_compose_file_path):
    _assert_git_executable_is_available()

    project_path = dirname(docker_compose_file_path)
    branch_name = _get_current_branch_name_in_path(project_path)
    return branch_name


def _get_current_branch_name_in_path(path):
    try:
        branch_reference = run_command(
            'git',
            ['symbolic-ref', '-q', 'HEAD'],
            cwd=path,
        )
    except SubprocessError:
        branch_name = None
    else:
        branch_name = branch_reference.split('/')[-1]
    return branch_name


def _assert_git_executable_is_available():
    try:
        run_command('git', ['--version'])
    except MissingCommandError as exc:
        raise VCSError('Git is not installed') from exc
