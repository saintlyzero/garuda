from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_queryset_creator
from api.models import Service
from typing import Optional, Any
from datetime import datetime


class ServiceStatusIn(BaseModel):
    id: int
    cpu_utilization: int
    memory_utilization: int


class ServiceStatusOut(BaseModel):
    id: int
    name: str
    cpu_utilization: Optional[int] = None
    memory_utilization: Optional[int] = None
    created_at: Optional[datetime] = None


ServicesOut = pydantic_queryset_creator(Service)
