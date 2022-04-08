from fastapi import APIRouter, UploadFile, File, status
import yaml
from exceptions import DuplicateServiceName, ServiceNotFound, ConfigFileError
from api.parse_file import NetworkGraph
from api.models import Service, ServiceStatus
from api.schemas import ServiceStatusIn, ServicesOut, ServiceStatusOut
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
