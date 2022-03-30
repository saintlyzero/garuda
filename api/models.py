from tortoise import fields, models
from api.parse_file import Node
from typing import List


class BaseModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
        app = "garuda"


class Service(BaseModel):
    name = fields.CharField(max_length=200)
    cpu_limit = fields.IntField()
    memory_limit = fields.IntField()

    @classmethod
    async def add_services(cls, graph: List[Node]) -> None:
        # add services
        services = {}
        for node in graph:
            service = await cls.create(
                name=node.name, cpu_limit=node.cpu_limit, memory_limit=node.memory_limit
            )
            services[node.name] = service

        # add links between services to represent as a graph
        for node in graph:
            to_service = services[node.name]
            for dependent in node.dependends:
                from_service = services[dependent.name]
                await ServiceEdge.create(
                    from_service=from_service, to_service=to_service
                )


class ServiceEdge(BaseModel):
    from_service = fields.ForeignKeyField(
        "garuda.Service", related_name="outgoing_edges"
    )
    to_service = fields.ForeignKeyField("garuda.Service", related_name="incoming_edges")

    class Meta:
        table = "service_edge"


class ServiceStatus(BaseModel):
    name = fields.CharField(max_length=200)
    service = fields.ForeignKeyField("garuda.Service")
    cpu_utilization = fields.IntField()
    memory_utilization = fields.IntField()
    created_at = fields.DatetimeField(null=False, auto_now_add=True)

    class Meta:
        table = "service_status"
