import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UpdateUserSchema(BaseModel):
    email: str | None = None
    telegram_id: int | None = None


class BaseUserSchema(UpdateUserSchema):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class CreateUserSchema(UpdateUserSchema):
    id: uuid.UUID
