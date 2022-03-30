from pydantic import BaseModel


class ServiceStatusIn(BaseModel):
    id: int
    cpu_utilization: int
    memory_utilization: int
