from typing import TypeVar, Type, Optional, Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.sql import Select
from .settings import get_settings

settings = get_settings()

# -------------------------- Base and Generic Type --------------------------
Base = declarative_base()
T = TypeVar("T")  # for "any SQLAlchemy model"

# -------------------------- Engine and Session --------------------------
engine = create_async_engine(settings.db.db_url, echo=True, future=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# -------------------------- FastAPI Dependency --------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Use this in FastAPI with Depends(get_db)
    Provides an async database session ready for queries
    """
    async with async_session() as session:
        yield session

# -------------------------- Generic CRUD Utilities --------------------------

async def create(instance: T) -> int:
    """Creates a record in the DB and returns the id"""
    async with async_session() as session:
        async with session.begin():
            session.add(instance)
            await session.flush()  # ensures instance.id is populated
            return instance.id

async def update(instance: T) -> int:
    """Updates an existing record and returns the id"""
    async with async_session() as session:
        async with session.begin():
            await session.merge(instance)
            await session.flush()
            return instance.id

async def update_fields(model: Type[T], id: int, data: dict) -> int:
    """Updates only specific fields of a record by its id"""
    async with async_session() as session:
        async with session.begin():
            instance = await session.get(model, id)
            if not instance:
                raise ValueError(f"{model.__name__} with id {id} not found")
            for key, value in data.items():
                setattr(instance, key, value)
            await session.flush()
            return instance.id

async def delete(instance: T) -> None:
    """Deletes a record"""
    async with async_session() as session:
        async with session.begin():
            await session.delete(instance)

async def delete_by_id(model: Type[T], id: int) -> None:
    """Deletes a record by its id"""
    async with async_session() as session:
        async with session.begin():
            stmt = sqlalchemy_delete(model).where(model.id == id)
            await session.execute(stmt)

async def fetch_one(query: Select) -> Optional[Any]:
    """Executes a query and returns a single result (or None)"""
    async with async_session() as session:
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def fetch_all(query: Select) -> list[Any]:
    """Executes a query and returns all results"""
    async with async_session() as session:
        result = await session.execute(query)
        return result.scalars().all()