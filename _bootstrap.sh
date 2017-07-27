##############################################################################
#
# Copyright (c) 2017, 2degrees Limited.
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

set -o nounset
set -o errexit
set -o pipefail


# ===== Utilities


function echo_stderr() {
    echo "$@" >&2
}


function error_out() {
    local exit_code="$1"
    local exit_message="$2"

    echo_stderr "$exit_message"
    return "$exit_code"
}
