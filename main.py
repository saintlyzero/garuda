from fastapi import FastAPI
from api.views import router as api_router
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="Garuda")


TORTOISE_CONFIG = {
    "connections": {
        "read_write": "postgres://root:root@localhost:5432/garuda",
    },
    "apps": {
        "garuda": {
            "models": [
                "api.models",
            ],
            "default_connection": "read_write",
        },
    },
}

# startup tasks


@app.on_event("startup")
async def init_db() -> None:
    """
    Initializes database with Tortoise ORM

    """

    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )


# shutdown tasks
@app.on_event("shutdown")
async def close_process() -> None:
    """
    Activities to perform on server shut-down
    - Close Tortoise DB Connection
    """
    await Tortoise.close_connections


@app.get("/ping")
async def root():
    return {"message": "pong"}


app.include_router(api_router)
