import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import get_settings
from .database import engine, Base
from .routers import routers
from .exceptions import register_exception_handlers

settings = get_settings()

app = FastAPI(
    title=settings.app.project_name,
    version=settings.app.api_version,
    docs_url="/docs"
)

register_exception_handlers(app)
routers(app)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.cors.allowed_methods,
    allow_headers=settings.cors.allowed_headers,
)


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to Contact Book API!"}

@app.get("/health", tags=["monitoring"])
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    await create_tables()
    print("🟢 App is starting up...")

@app.on_event("shutdown")
async def on_shutdown():
    print("🔴 App is shutting down...")