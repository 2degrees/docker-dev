from pkg_resources import iter_entry_points


def get_objects_in_entry_point_group(group_name):
    objects_by_name = {}
    for entry_point in iter_entry_points(group_name):
        objects_by_name[entry_point.name] = entry_point.load()
    return objects_by_name
