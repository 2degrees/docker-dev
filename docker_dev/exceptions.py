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


class DockerDevUtilsException(Exception):
    pass


class VCSError(DockerDevUtilsException):
    pass


class SubprocessError(DockerDevUtilsException):

    def __init__(self, command_args, return_code):
        super(SubprocessError, self).__init__()

        self._command_args = command_args
        self._return_code = return_code

    def __str__(self):
        command_str = ' '.join(self._command_args)
        error_string = '`{}` exited with code {}'.format(
            command_str,
            self._return_code,
        )
        return error_string


class MissingCommandError(DockerDevUtilsException):

    def __init__(self, command_name):
        super(MissingCommandError, self).__init__()

        self._command_name = command_name

    def __str__(self):
        error_string = \
            'Command {!r} was not found in $PATH'.format(self._command_name)
        return error_string


class PluginError(DockerDevUtilsException):

    def __init__(self, plugin_name):
        super(PluginError, self).__init__()

        self._plugin_name = plugin_name

    def __str__(self):
        error_string = 'Plugin {!r} failed'.format(self._plugin_name)
        return error_string
