from setuptools import setup
import setuptools

setup(
    name='adf-validator',
    version='0.0.1',
    description='Azure Data Factory GIT based validation',
    author='Nadav Har Tzvi',
    url='https://github.com/nadav-har-tzvi/adf-validator',
    install_requires=[
        'marshmallow==3.14.0',
        'marshmallow-oneofschema==3.0.1', 
        'click==8.0.3', 
        'GitPython==3.1.24'
    ],
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": [
            "validate-adf = adf_validator.cli:main"
        ]
    }
)