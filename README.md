# Development tool for Docker and Docker Compose

`docker-dev` eases common tasks involving Docker and Docker Compose in
development. **Its primary feature is to namespace Docker Compose projects** so
that you can easily have one project for each branch in your repository.

Docker Compose projects are given a name, which default to that of the project
directory. This name is then prefixed to the Docker resources (e.g., images,
containers) created for the Docker Compose project.

`docker-dev` extends the project name to include the active branch name, and
then proxies calls to `docker-compose` so that they refer to the new project
name. For example, if your project is called "foo" and your active Git branch
is "master", the Docker Compose project name will be set to "foo-master".

This tool is available on PYPI as
[docker-dev](https://pypi.python.org/pypi/docker-dev).

## Features

- Maintain isolated Docker Compose projects for branches of the same VCS
  repository, even if they all share the same path. This means that
  `git checkout` will play nice with `docker-compose`.
- Run host-level commands just before running `docker-compose build`. This is
  essential in some environments, such as Python where a `*.egg-info` directory
  must exist at the root of the project if you mount the path on the container
  to get instant code reload.
- Easily run your test suites and export their output to the host. For example,
  you can use this to expose your test reports to your Continuous Integration
  Service.

## Development

`docker-dev` proxies the `docker-compose` sub-commands `build`, `up` and `down`:

- `docker-dev build` will run all the pre-build hooks that you have
  installed (see below) and it'll also pull the latest version of any base
  images before actually building the images.
- `docker-dev up` ensures that you get new containers on each call.
- `docker-dev down` ensures that no trace of your project is left in Docker
  (inc. images, containers and volumes).

## Testing

`docker-dev test` allows you to run test suites and export their output to the
host system. It requires a Docker Compose file (`testing.dc.yml` by default)
that defines all the services responsible for running the tests.

Each test service has to begin with "test-" and must place its output in
`/tmp/test-reports`, as the contents of this directory will later be exported to
the host. Here's an example of a Docker Compose file for testing:

```yaml
version: "2"
services:
  test-main:
    build: "."
    command: "test-runner --output-dir=/tmp/test-reports"
```

To prevent a name clash, the suffix "-test" is added to the Docker Compose
project name when run.

No traces are left in Docker after this command is run, not even when the tests
fail.

## Plugins

This tool can be extended via the following types of plugins.

### Project Name Suffix Generator

If your Docker Compose project is in a Git repository, `docker-dev` will append
the active branch name to the name of the Docker Compose project. If you want
to override this behaviour or add support for another VCS, you'd need to create
a function that computes the suffix; e.g.:

```python
def get_project_name_suffix(docker_compose_file_path):
    return 'suffix'
```

Finally, you have to register that function in your project's `setup.py` file
as an entry point for the group `docker_dev.project_name_suffix`. E.g.,

```python
setup(
    name='your-distribution',
    entry_points={
        'docker_dev.project_name_suffix': [
            'foo = your_package:get_project_name_suffix',
        ],
    },
)

```

### Pre-Build Hook

To have routines executed at the host level before building the images, you
can create a pre-build hook. For example:

```python
def hook(docker_compose_file_path, project_name):
    run_some_commands()
```

This function then has to be registered as an entry point, under the group
`docker_dev.pre_build_hooks`.

`docker-dev` will run all the installed pre-build hooks unconditionally.

As of this writing, only one plugin is available:
[docker-dev-python](https://github.com/2degrees/docker-dev-python).

## CLI

For an comprehensive and up-to-date description of the CLI, run
`docker-dev --help`.
