from typing import List


class DataFactoryConfigurationSet:
    factory: dict
    managed_vnet: dict
    pipelines: List[dict]
    datasets: List[dict]
    linked_services: List[dict]
    integration_runtimes: List[dict]

    def __init__(self) -> None:
        self.factory = None
        self.managed_vnet = None
        self.pipelines = []
        self.datasets = []
        self.linked_services = []
        self.integration_runtimes = []
