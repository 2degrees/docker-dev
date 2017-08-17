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

### docker-dev

`docker-dev` wraps some Docker Compose subcommands in order to pass extra
arguments. It's not opinionated about the structure of your Docker Compose
file, and you can switch between `docker-dev` and `docker-compose`.

`docker-dev` supports autocompletion in a Bash session.

#### `docker-dev build [EXTRA_ARGS...]`

Wraps `docker-compose build`, and also:

- Avoids leaving intermediate containers behind.
- Pulls the latest version of any parent Docker images.
- If an executable file called `.dockerdev-prebuild` exists in the current
  working directory, it'll be run before running `docker-compose build` (unless
  the executable fails).

#### `docker-dev run [EXTRA_ARGS...]`

Wraps `docker-compose run` to prevent leaving containers behind once the
command ends.

#### `docker-dev up [EXTRA_ARGS...]`

Wraps `docker-compose up` and prevents leaving containers behind once the
command ends and to exit once any of the services explicitly called exits.

#### `docker-dev up2 [SERVICES...]`

**Experimental:** This subcommand is expected to replace `docker-dev up`
eventually, and it will be changed or simply removed in future releases.

This subcommand wraps `docker-dev up` and works around limitations in Docker
Compose when the services you want to run depend on other services -- namely:

- Logs from dependent services are output in the foreground.
- Terminating the `docker-dev` process also terminates dependent services.
- Likewise, when a dependent service terminates, all the other services and
  the parent process are terminated.

#### `docker-dev down`

Runs `docker-compose down` so that all the resources in the project are removed.

## docker-clean

This command will remove **all** your Docker resources (e.g., containers,
volumes), except for images created in the past week.
