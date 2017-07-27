# docker-dev: Utilities to use Docker in development environments

`docker-dev` optimises Docker and Docker Compose for use on a developer's
computer, making some common tasks easier than they would be otherwise.

Once you've cloned or downloaded this project, you can enable it by adding
the following line to `~/.bashrc`:

```bash
source /path-to-dockerdev/dockerdevrc
```

## Commands

The following Bash scripts are included:

### `docker-dev`

`docker-dev` wraps some Docker Compose subcommands in order to pass extra
arguments. It's not opinionated about the structure of your Docker Compose
file, and you can switch between `docker-dev` and `docker-compose`.

The `docker-compose` subcommands wrapped are:

- `build`, to avoid leaving intermediate containers and also pull the latest
  version of any parent Docker images. If an executable file called
  `.dockerdev-prebuild` exists in the current working directory, it'll be
  run before running `docker-compose build` (unless the executable fails).
- `run`, to prevent leaving containers behind once the command ends.
- `up`, to prevent leaving containers behind once the command ends and to
  exit once a container exists.
- `down`, to force Docker Compose to remove all the resources in the project.

For example,

```bash
docker-dev build webapp
```

`docker-dev` supports autocompletion in a Bash session.

## `docker-clean`

This command will remove **all** your Docker resources (e.g., containers,
volumes), except for images created in the past week.
