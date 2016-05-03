from pyrecord import Record

from docker_dev_utils.exceptions import ConfigurationError
from docker_dev_utils.plugins import get_objects_in_entry_point_group


RepositoryInfo = Record.create_type('RepositoryInfo', 'path', 'branch_name')


def get_repository_info_from_path(path):
    repository_info_finders = get_objects_in_entry_point_group(
        'docker_dev_utils.vcs_repository_finders',
    )
    for repository_info_finder in repository_info_finders.values():
        repository_info = repository_info_finder(path)
        if repository_info:
            break
    else:
        repository_info = None

    if not repository_info:
        error_message = \
            'Could not find a repository at or above {!r}'.format(path)
        raise ConfigurationError(error_message)

    return repository_info
