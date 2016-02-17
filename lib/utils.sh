# Miscellaneous Bash functions


function echo_stderr() {
    echo "$@" >&2
}


function error_out() {
    local exit_code=$1
    local exit_message=$2

    echo_stderr "$exit_message"
    exit "$exit_code"
}


function assert_inside_git_worktree() {
    if ! git rev-parse --show-toplevel >>/dev/null 2>&1; then
        error_out 1 "Current directory is not a Git working tree"
    fi
}


function get_project_root_path() {
    assert_inside_git_worktree
    git rev-parse --show-toplevel
}


function get_project_branch() {
    assert_inside_git_worktree

    local branch_name
    branch_name="$(git symbolic-ref -q HEAD)"
    branch_name="${branch_name##refs/heads/}"
    branch_name="${branch_name:-HEAD}"
    echo "${branch_name}"
}


function get_project_name() {
    local project_name

    project_name="$(basename "$(get_project_root_path)")-$(get_project_branch)"
    echo "${project_name}"
}
