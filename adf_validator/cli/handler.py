from typing import List
from .models.dataset import DataSet
from .models.factory import Factory
from .models.input import DataFactoryConfigurationSet
from .models.linked_service import LinkedService
from .models.managed_vnet import ManagedVirtualNetwork
from .models.pipeline import Pipeline

def validate_factory(factory_data: dict) -> Factory:
    return Factory().load(factory_data)

def validate_vnet(vnet_data: dict) -> ManagedVirtualNetwork:
    return ManagedVirtualNetwork().load(vnet_data)

def validate_linked_services(linked_services_data: List[dict]) -> List[LinkedService]:
    return [LinkedService().load(ls_data) for ls_data in linked_services_data]

def validate_datasets(datasets_data: List[dict]) -> List[DataSet]:
    return [DataSet().load(dataset_data) for dataset_data in datasets_data]

def validate_pipelines(pipelines_data: List[dict]):
    return [Pipeline().load(pipeline_data) for pipeline_data in pipelines_data]

def validate_data_factory(adf_data: DataFactoryConfigurationSet):
    validate_factory(adf_data.factory)
    validate_vnet(adf_data.managed_vnet)
    validate_linked_services(adf_data.linked_services)
    validate_datasets(adf_data.datasets)
    validate_pipelines(adf_data.pipelines)