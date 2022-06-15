from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_queryset_creator
from api.models import Service
from typing import Optional, List
from datetime import datetime


class ServiceStatusIn(BaseModel):
    id: int
    cpu_utilization: float
    memory_utilization: float


class ServiceStatusOut(BaseModel):
    id: int
    name: str
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    created_at: Optional[datetime] = None


ServicesOut = pydantic_queryset_creator(Service)


class GraphService(BaseModel):
    id: int
    name: str
    cpu_limit: float
    memory_limit: float
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    edges: List[int] = []
    is_healthy: Optional[int] = None


class GraphEdge(BaseModel):
    source: str
    target: str


class SankyGraphOut(BaseModel):
    nodes: List[GraphService]
    edges: List[GraphEdge]
