import typing
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_mixin, declared_attr

from .base_model import Base, BaseDBMixin
from .enums import CloudMessageTypes, BrowserTypes


class Device(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    name: Mapped[str | None]
    active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    application_id: Mapped[str | None] = mapped_column(String(length=64))
    device_id: Mapped[typing.Optional[str]] = mapped_column(default=None, index=True)
    registration_id: Mapped[str] = mapped_column(unique=True)

    # @declared_attr
    # def user_fcm(self) -> Mapped["User"]:
    #     return relationship(back_populates='fcm_devices')
    #
    # @declared_attr
    # def user_web_push(self) -> Mapped["User"]:
    #     return relationship(back_populates='web_push_devices')


class User(BaseDBMixin, Base):
    email: Mapped[str | None]
    telegram_id: Mapped[int | None] = mapped_column(unique=True)
    fcm_devices: Mapped[typing.List["GCMDevice"]] = relationship(
                                                          cascade="all, delete")
    web_push_devices: Mapped[typing.List["WebPushDevice"]] = relationship(
                                                          cascade="all, delete")



class GCMDevice(Device):
    cloud_message_type: Mapped[CloudMessageTypes] = mapped_column(default=CloudMessageTypes.FCM)


class APNSDevice(Device):
    registration_id: Mapped[str] = mapped_column(String(length=200))


class WNSDevice(Device):
    pass


class WebPushDevice(Device):
    p256dh: Mapped[str] = mapped_column(String(length=88))
    auth: Mapped[str] = mapped_column(String(length=24))
    browser: Mapped[BrowserTypes]
