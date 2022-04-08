from fastapi import APIRouter, UploadFile, File, status
import yaml
from exceptions import DuplicateServiceName, ServiceNotFound, ConfigFileError
from api.parse_file import NetworkGraph
from api.models import Service, ServiceStatus, ServiceEdge
from api.schemas import ServiceStatusIn, ServicesOut, ServiceStatusOut, GraphServiceOut
from tortoise import Tortoise
from typing import List

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_content = await file.read()
    try:
        graph = NetworkGraph(file_content).create_graph()
        await Service.add_services(graph)
        print(graph)
    except yaml.YAMLError as e:
        raise ConfigFileError(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid YAML file"
        ) from e
    except (DuplicateServiceName, ServiceNotFound) as e:
        raise ConfigFileError(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
    return {"Filename": file.filename}


@router.post("/status")
async def status(params: ServiceStatusIn):
    service: Service = await Service.get(id=params.id)
    await ServiceStatus.create(
        service=service,
        cpu_utilization=params.cpu_utilization,
        memory_utilization=params.memory_utilization,
    )
    return params


@router.get("/status", response_model=List[ServiceStatusOut])
async def get_status():
    DB_CONNECTION = Tortoise.get_connection("read_write")

    return await ServiceStatus.get_all_service_status(DB_CONNECTION)


@router.get("/service", response_model=ServicesOut)
async def get_service():
    return await ServicesOut.from_queryset(Service.all())


# @router.get("/graph")
@router.get("/graph", response_model=List[GraphServiceOut])
async def get_dependency_graph():
    DB_CONNECTION = Tortoise.get_connection("read_write")

    services = await Service.all()
    service_status = await ServiceStatus.get_all_service_status(DB_CONNECTION)
    service_edges = await ServiceEdge.all()

    graph = {}
    # add all services to graph
    for service in services:
        node = GraphServiceOut(
            id=service.id,
            name=service.name,
            cpu_limit=service.cpu_limit,
            memory_limit=service.memory_limit,
        )
        graph[service.id] = node

    # add edges
    for edge in service_edges:
        graph[edge.from_service_id].edges.append(edge.to_service_id)

    # check service status and cascade failing service status
    unhealthy_services = []
    for service in service_status:
        node = graph[service["id"]]
        node.cpu_utilization = service["cpu_utilization"]
        node.memory_utilization = service["memory_utilization"]

        # services with not status available
        if node.cpu_utilization is None:
            continue

        # healthy = 1 | unhealthy = 0
        node.is_healthy = (
            0
            if node.cpu_utilization > node.cpu_limit
            or node.memory_utilization > node.memory_limit
            else 1
        )
        if not node.is_healthy:
            unhealthy_services.append(service["id"])

    # update status of services dependent on unhealthy services
    for id in unhealthy_services:
        node = graph[id]
        for dependent_node_id in node.edges:
            graph[dependent_node_id].is_healthy = 0

    return list(graph.values())
