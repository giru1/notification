import typing

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import update, select, delete

from db.session import async_session_maker
from models.base_model import Base
from models.user import User
from sqlalchemy.exc import IntegrityError

ModelType = typing.TypeVar('ModelType', bound=Base)
CreateSchemaType = typing.TypeVar('CreateSchemaType', bound=BaseModel)


class BaseDeviceRepository:
    def __init__(self, model: typing.Type[ModelType],
                 create_schema: typing.Type[CreateSchemaType],
                 user: User) -> None:
        self.model = model
        self.create_schema = create_schema
        self.user = user

    async def get_devices_by_user(self):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == self.user.id,
                                            self.model.active == True)
            result = await session.execute(stmt)
            scalars = result.scalars()
            return [obj for obj in scalars.all()]

    async def deactivate_device_by_id(self, device_id: int):
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == device_id).values(active=False)
            await session.execute(stmt)
            await session.commit()
            obj = await self.get_obj(device_id)
            return obj

    async def get_by_id(self, obj_id: int) -> ModelType:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == obj_id,
                                            self.model.user_id == self.user.id)
            result = await session.execute(stmt)
            obj = result.unique().scalar_one_or_none()
            if obj is None:
                raise HTTPException(status_code=404, detail="Object not found")
            return obj

    async def get_obj(self, obj_id) -> ModelType:
        async with async_session_maker() as session:
            result = await session.get(self.model, obj_id)
            return result

    async def create(self, data) -> ModelType:
        async with async_session_maker() as session:
            try:
                obj = self.model(**data.model_dump())
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
            except IntegrityError:
                session.rollback()
                raise HTTPException(status_code=400, detail="Object already exists")
            return obj

    async def delete(self, obj_id: int) -> int:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == obj_id,
                                            self.model.user_id == self.user.id)
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Object not found")
            await session.commit()
            return obj_id

