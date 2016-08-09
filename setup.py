from os import path

from setuptools import find_packages
from setuptools import setup


_HERE = path.abspath(path.dirname(__file__))
_VERSION = open(path.join(_HERE, 'VERSION.txt')).readline().rstrip()
_README = open(path.join(_HERE, 'README.rst')).read().strip()


setup(
    name='docker-dev-utils',
    version=_VERSION,
    description='Development tools for Docker',
    long_description=_README,
    url='https://pythonhosted.org/docker-dev-utils/',
    author='2degrees',
    author_email='2degrees-floss@googlegroups.com',
    classifiers=[],
    keywords='',
    license='',
    packages=find_packages(),
    install_requires=[
        'click == 6.6',
        'pyrecord == 1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'docker-dev-utils = docker_dev_utils.cli:main',
        ],
        'docker_dev_utils.vcs_repository_finders': [
            'git = docker_dev_utils.plugins.git_integration:get_repository_info_from_path',
        ],
    },
)
