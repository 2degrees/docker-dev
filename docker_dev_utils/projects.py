from docker_dev_utils.docker_interface import run_docker_compose_subcommand
from docker_dev_utils.exceptions import VCSError, PluginError
from docker_dev_utils.plugins import get_objects_in_entry_point_group


def install_project(project_path, project_name):
    _run_host_pre_build_hooks(project_path, project_name)

    run_docker_compose_subcommand(
        'build',
        ['--pull'],
        project_path,
        project_name,
    )


def _run_host_pre_build_hooks(project_path, project_name):
    hooks = get_objects_in_entry_point_group('pre_build_hooks').items()
    for hook_name, hook in hooks:
        try:
            hook(project_path, project_name)
        except Exception as exc:
            raise PluginError(hook_name) from exc


def uninstall_project(project_path, project_name):
    run_docker_compose_subcommand(
        'down',
        ['--rmi=all', '--volumes'],
        project_path,
        project_name,
    )


def get_project_name_refinement(path):
    project_name_refiners = get_objects_in_entry_point_group(
        'project_name_refiners',
    )
    project_name_refinement = None
    for project_name_refiner in project_name_refiners.values():
        try:
            project_name_refinement = project_name_refiner(path)
        except VCSError:
            continue
        else:
            break
    return project_name_refinement
