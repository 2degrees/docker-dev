from os import path

from setuptools import find_packages
from setuptools import setup


_HERE = path.abspath(path.dirname(__file__))
_VERSION = open(path.join(_HERE, 'VERSION.txt')).readline().rstrip()
_README = open(path.join(_HERE, 'README.rst')).read().strip()


setup(
    name='docker-dev',
    version=_VERSION,
    description='Development tools for Docker',
    long_description=_README,
    author='2degrees',
    author_email='2degrees-floss@googlegroups.com',
    classifiers=[],
    keywords='',
    license='',
    packages=find_packages(),
    install_requires=[
        'click == 6.6',
        'PyYAML == 3.11',
    ],
    entry_points={
        'console_scripts': [
            'docker-dev = docker_dev.cli:main',
        ],
        'docker_dev.project_name_refiners': [
            'git = docker_dev.plugins.git_integration:get_active_branch_name',
        ],
        'docker_dev.pre_build_hooks': [
            'python = docker_dev.plugins.python_dev:build_python_distributions',
        ],
    },
)
