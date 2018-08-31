
import os

from setuptools import setup, find_packages


# -- REQUIREMENTS
requirements_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')


def parse_requirements(requirements):

    return [
        r.strip()
        for r in requirements
        if (
            not r.strip().startswith('#') and
            not r.strip().startswith('-e') and
            r.strip())
    ]


with open(requirements_path) as f:
    requirements = parse_requirements(f.readlines())


setup(
    name='Logger',
    version='0.0.4',
    description='Logger integrating one with Application Insights',
    url='https://git.viessmann.com/projects/DEC/repos/logger',
    author='Viessmann Data Chapter Team',
    author_email='data-engineers@viessmann.com',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False)
