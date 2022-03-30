from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
        app = "garuda"


class Service(BaseModel):
    name = fields.CharField(max_length=200)
    type = fields.CharField(max_length=100)
    cpu_limit = fields.IntField()
    memory_limit = fields.IntField()


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
