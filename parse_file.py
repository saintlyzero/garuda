import logging

from exceptions import DuplicateServiceName, ServiceNotFound
from typing import Set, Dict, List
from utils import read_yaml

class Node:
    def __init__(self, name:str, cpu_limit:int=80, memory_limit:int=80) -> None:
        self.name:str = name
        self.cpu_limit:int = cpu_limit
        self.memory_limit:int = memory_limit
        self.dependends: Set["Node"] = set()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.name} --> {self.dependends}"
    

class NetworkGraph:
    def __init__(self, filename:str) -> None:
        self.filename:str = filename
        self.services:List[Node] = []
        
    def create_graph(self):
        file_content = read_yaml(self.filename)
        services = file_content.get("services", [])
        dependency = file_content.get("dependency", [])
        self.services = self.build_graph(services, dependency)
        print(self.services)


    def build_graph(self, nodes:List[dict], dependencies:List[dict]) -> List[Node]:

        # add nodes to graph
        graph: Dict[Node] = {}
        for  node in nodes:
            name, cpu_limit, memory_limit = node.values()
            if name in graph:
                logging.error(f"duplicate service-name: {name}")
                raise DuplicateServiceName()

            graph[name] = Node(name, cpu_limit=cpu_limit, memory_limit=memory_limit)


        # add dependencies for each node
        for dependency in dependencies:
            name = dependency.get("tag")
            depends_on = dependency.get("requires", [])
            node:Node = graph.get(name)
            if not node:
                logging.error(f"service {name} not found while adding dependency")
                raise ServiceNotFound()

            for service_name in depends_on:
                dependent_node:Node = graph.get(service_name)
                if not dependent_node:
                    logging.error(f"service {service_name} not found in nodes while it is present under requires field of {name}")
                    raise ServiceNotFound()
                node.dependends.add(dependent_node)

        return graph.values()


def main():
    NetworkGraph("network-config.yaml").create_graph()

if __name__ == "__main__":
    main()