##############################################################################
#
# Copyright (c) 2016, 2degrees Limited.
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
from functools import wraps as wrap_function

import click
from click.globals import get_current_context
from docker_dev.exceptions import DockerDevUtilsException


def _fail(exc):
    click.echo('Error: ' + str(exc), err=True)
    context = get_current_context()
    context.exit(1)


def handle_callback_exception(callback_original):
    @wrap_function(callback_original)
    def callback_wrapped(*args, **kwargs):
        try:
            return callback_original(*args, **kwargs)
        except DockerDevUtilsException as exc:
            _fail(exc)

    return callback_wrapped
