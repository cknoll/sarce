from setuptools import setup, find_packages

from sarce.release import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()


with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read()


setup(
    name='sarce',
    author="Carsten Knoll",
    author_email='carsten.knoll@posteo.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    description="state aware remote command execution - layer on top of fabric to execute commands with a state",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n',
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='ssh, remote execution',
    packages=find_packages(),
    version=__version__,
)
