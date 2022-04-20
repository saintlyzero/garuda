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
    cpu_utilization: Optional[int] = None
    memory_utilization: Optional[int] = None
    created_at: Optional[datetime] = None


ServicesOut = pydantic_queryset_creator(Service)


class GraphService(BaseModel):
    id: int
    name: str
    cpu_limit: int
    memory_limit: int
    cpu_utilization: Optional[int] = None
    memory_utilization: Optional[int] = None
    edges: List[int] = []
    is_healthy: Optional[int] = None


class GraphEdge(BaseModel):
    source: str
    target: str


class SankyGraphOut(BaseModel):
    nodes: List[GraphService]
    edges: List[GraphEdge]
