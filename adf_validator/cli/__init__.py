import glob
import click
import json
import tempfile
from git import Repo
from .handler import validate_data_factory

from .models.input import DataFactoryConfigurationSet


def load_adf_configuration(configuration_path: str) -> DataFactoryConfigurationSet:
    adf_data = DataFactoryConfigurationSet()
    for file_path in glob.glob(f'{configuration_path}/**/*.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            if 'pipeline' in file_path:
                adf_data.pipelines.append(data)
            elif 'dataset' in file_path:
                adf_data.datasets.append(data)
            elif 'linkedService' in file_path:
                adf_data.linked_services.append(data)
            elif 'integrationRuntime' in file_path:
                adf_data.integration_runtimes.append(data)
            elif 'managedVirtualNetwork' in file_path:
                adf_data.managed_vnet = data
            elif 'factory' in file_path:
                adf_data.factory = data
    return adf_data

@click.command(help='Validates ADF configuration from a git repo located at URL')
@click.argument('url')
def validate(url):
    with tempfile.TemporaryDirectory() as tmpdir:
        Repo.clone_from(url, tmpdir)
        adf_data = load_adf_configuration(tmpdir)
        validate_data_factory(adf_data)

def main():
    validate()