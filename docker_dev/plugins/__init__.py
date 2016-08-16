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
from pkg_resources import iter_entry_points


_ROOT_GROUP_NAME = 'docker_dev'


def get_objects_in_entry_point_group(subgroup_name):
    group_name = '{}.{}'.format(_ROOT_GROUP_NAME, subgroup_name)
    objects_by_name = {}
    for entry_point in iter_entry_points(group_name):
        objects_by_name[entry_point.name] = entry_point.load()
    return objects_by_name
