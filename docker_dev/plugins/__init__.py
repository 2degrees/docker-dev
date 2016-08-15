from pkg_resources import iter_entry_points


_ROOT_GROUP_NAME = 'docker_dev'


def get_objects_in_entry_point_group(subgroup_name):
    group_name = '{}.{}'.format(_ROOT_GROUP_NAME, subgroup_name)
    objects_by_name = {}
    for entry_point in iter_entry_points(group_name):
        objects_by_name[entry_point.name] = entry_point.load()
    return objects_by_name
