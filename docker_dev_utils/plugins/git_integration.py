from locale import getpreferredencoding
from subprocess import CalledProcessError
from subprocess import check_output as run_command

from docker_dev_utils.exceptions import VCSError
from docker_dev_utils.vcs import RepositoryInfo


_SYSTEM_ENCODING = getpreferredencoding()


def get_repository_info_from_path(path):
    _assert_git_executable_is_available()

    worktree_path = _get_git_worktree_path_from_path(path)
    if worktree_path:
        branch_name = _get_current_branch_name_in_worktree(worktree_path)
        repository_info = RepositoryInfo(worktree_path, branch_name)
    else:
        repository_info = None
    return repository_info


def _get_git_worktree_path_from_path(path):
    try:
        worktree_path = \
            _run_command_str(['git', 'rev-parse', '--show-toplevel'], cwd=path)
    except CalledProcessError:
        worktree_path = None
    return worktree_path


def _get_current_branch_name_in_worktree(worktree_path):
    branch_reference = _run_command_str(
        ['git', 'symbolic-ref', '-q', 'HEAD'],
        cwd=worktree_path,
    )
    branch_name = branch_reference.split('/')[-1]
    return branch_name


def _run_command_str(*args, **kwargs):
    stdout_bytes = run_command(*args, **kwargs)
    stdout_str = stdout_bytes.decode(_SYSTEM_ENCODING)
    return stdout_str.rstrip()


def _assert_git_executable_is_available():
    try:
        run_command(['git', '--version'])
    except CalledProcessError:
        raise VCSError('Git is not installed')
