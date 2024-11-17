import typing

from pydantic import BaseModel

from schemas.register_device import TypeDevice


class SendMessageSchema(BaseModel):
    message: str


class SendMessageByTypeDeviceSchema(SendMessageSchema):
    type_device: typing.Optional[TypeDevice] = None


class SendMessageByDeviceRabbitSchema(BaseModel):
    user_id: str
