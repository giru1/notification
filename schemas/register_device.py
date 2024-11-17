from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from schemas.device import CreateDeviceSchema, FCMDeviceSchema, WebPushDeviceSchema


class TypeDevice(str, Enum):
    webpush = 'webpush'
    fcm = 'fcm'
    email = 'email'
    telegram = 'telegram'


class RegisterDeviceSchema(BaseModel):
    user_id: UUID
    device_type: TypeDevice
    device: FCMDeviceSchema | WebPushDeviceSchema

