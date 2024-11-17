import typing

from fastapi import HTTPException
from sqlalchemy import update, select

from db.session import async_session_maker
from models.user import User
from schemas.user import CreateUserSchema
from services.base import ModelType, CreateSchemaType


class UserRepository:
    def __init__(self, model: User,
                 create_schema: typing.Type[CreateSchemaType]) -> None:
        self.model = model
        self.create_schema = create_schema

    async def create_user(self, data) -> ModelType:
        async with async_session_maker() as session:
            obj = self.model(**data.model_dump())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def get_obj(self, obj_id) -> ModelType:
        async with async_session_maker() as session:
            result = await session.get(self.model, obj_id)
            return result

    async def update(self, obj_id: str, data) -> ModelType:
        async with async_session_maker() as session:
            stmt = (update(self.model)
                    .where(self.model.id == obj_id)
                    .values(**data.model_dump(exclude_none=True, exclude_unset=True)))
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Object not found")
            await session.commit()
            obj = await self.get_obj(obj_id)
            return obj

    async def get_all(self):
        async with async_session_maker() as session:
            stmt = (select(self.model))
            result = await session.execute(stmt)
            scalars = result.scalars()
            return scalars.all()

def get_user_repository():
    return UserRepository(model=User, create_schema=CreateUserSchema)
