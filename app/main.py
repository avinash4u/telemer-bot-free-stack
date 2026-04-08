from fastapi import FastAPI
from app.routers import health, calls
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.db import Base, engine
from app.clients.freeswitch import fs_client

configure_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TeleMER Voice Bot Orchestrator", version="1.0.0")
app.include_router(health.router)
app.include_router(calls.router, prefix="/calls", tags=["calls"])

@app.on_event("startup")
async def startup_event():
    # Connect to FreeSWITCH when app starts
    fs_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    # Disconnect from FreeSWITCH when app shuts down
    fs_client.disconnect()

@app.get("/")
def root():
    return {
        "service": "telemer-orchestrator",
        "env": settings.app_env,
        "docs": "/docs",
    }
