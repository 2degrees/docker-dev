class DockerDevUtilsException(Exception):
    pass


class VCSError(DockerDevUtilsException):
    pass


class ConfigurationError(DockerDevUtilsException):
    pass
