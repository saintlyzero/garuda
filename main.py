from fastapi import FastAPI
from api.views import router as api_router

app = FastAPI(title="Garuda")



TORTOISE_CONFIG = {
    "connections": {
        "read_write": "FOO-BAR",
    },
    "apps": {
        "garuda": {
            "models": [
                "aerich.models",
            ],
            "default_connection": "read_write",
        },
    },
}

@app.get("/ping")
async def root():
    return {"message": "pong"}

app.include_router(api_router)