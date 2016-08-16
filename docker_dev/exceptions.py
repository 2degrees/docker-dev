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
class DockerDevUtilsException(Exception):
    pass


class VCSError(DockerDevUtilsException):
    pass


class SubprocessError(DockerDevUtilsException):

    def __init__(self, command_args, return_code, stderr_bytes):
        super(SubprocessError, self).__init__()

        self._command_args = command_args
        self._return_code = return_code
        self._stderr_bytes = stderr_bytes

    def __str__(self):
        command_str = ' '.join(self._command_args)
        stderr_str = self._stderr_bytes.decode().strip()
        error_string = '`{}` exited with code {}.\n\nstderr:\n{}'.format(
            command_str,
            self._return_code,
            stderr_str,
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
