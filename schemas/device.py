import typing
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.enums import BrowserTypes


class CreateDeviceSchema(BaseModel):
    name: typing.Optional[str] = None
    active: bool = True
    user_id: typing.Optional[UUID] = None
    application_id: typing.Optional[str] = None
    device_id: typing.Optional[str] = None
    registration_id: str


class BaseDeviceSchema(CreateDeviceSchema):
    id: int
    created_at: datetime


class FCMDeviceSchema(CreateDeviceSchema):
    pass


class BaseFCMDeviceSchema(BaseDeviceSchema):
    pass


class WebPushDeviceSchema(CreateDeviceSchema):
    p256dh: str
    auth: str
    browser: str


class BaseWebPushDeviceSchema(BaseFCMDeviceSchema):
    p256dh: str
    auth: str
    browser: BrowserTypes = BrowserTypes.CHROME
