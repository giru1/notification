from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.orm import declarative_mixin

from utils.utils import change_case


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return change_case(cls.__name__)


@declarative_mixin
class BaseDBMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
