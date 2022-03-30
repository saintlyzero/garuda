import logging
import yaml
from exceptions import DuplicateServiceName, ServiceNotFound
from typing import Set, Dict, List

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
    def __init__(self, file_content:str) -> None:
        self.file_content:str = file_content
        self.services:List[Node] = []
        
    def create_graph(self):
        parsed_content = {}
        parsed_content = yaml.safe_load(self.file_content)
        services = parsed_content.get("services", [])
        dependency = parsed_content.get("dependency", [])
        self.services = self.build_graph(services, dependency)


    def build_graph(self, nodes:List[dict], dependencies:List[dict]) -> List[Node]:

        # add nodes to graph
        graph: Dict[Node] = {}
        for  node in nodes:
            name, cpu_limit, memory_limit = node.values()
            if name in graph:
                raise DuplicateServiceName(f"duplicate service-name: {name}")

            graph[name] = Node(name, cpu_limit=cpu_limit, memory_limit=memory_limit)


        # add dependencies for each node
        for dependency in dependencies:
            name = dependency.get("tag")
            depends_on = dependency.get("requires", [])
            node:Node = graph.get(name)
            if not node:
                raise ServiceNotFound(f"service {name} not found while adding dependency")

            for service_name in depends_on:
                dependent_node:Node = graph.get(service_name)
                if not dependent_node:
                    raise ServiceNotFound(f"service {service_name} not found in nodes while it is present under requires field of {name}")
                node.dependends.add(dependent_node)

        return graph.values()