import typing

from pydantic import BaseModel

from models.enums import CloudMessageTypes
from schemas.device import CreateDeviceSchema


class WebPushResultSchema(BaseModel):
    original_registration_id: str
    success: bool
    error_message: typing.Optional[str] = None


class CreateGCMDeviceSchema(CreateDeviceSchema):
    cloud_message_type: CloudMessageTypes = CloudMessageTypes.FCM


class CreateAPNSDeviceSchema(CreateDeviceSchema):
    pass


class CreateWebPushDeviceSchema(CreateDeviceSchema):
    p256dh: str
    auth: str
    browser: str
