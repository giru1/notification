import typing
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.user import GCMDevice, WebPushDevice, Device
from schemas.device import FCMDeviceSchema, WebPushDeviceSchema, BaseFCMDeviceSchema, BaseWebPushDeviceSchema, \
    CreateDeviceSchema, BaseDeviceSchema
from schemas.register_device import RegisterDeviceSchema, TypeDevice
from schemas.send_message import SendMessageSchema, SendMessageByTypeDeviceSchema
from schemas.user import CreateUserSchema, BaseUserSchema, UpdateUserSchema
from services.base import BaseDeviceRepository
from services.gcm_service import GCMPushNotificationService
from services.user import get_user_repository, UserRepository
from services.webpush_service import WebPushNotificationService

device_router = APIRouter(prefix="/notification", tags=["device"])


@device_router.post("/user/register", response_model=BaseUserSchema)
async def register_user(user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)], data: CreateUserSchema):
    user = await user_service.get_obj(data.id)
    if user:
        return user
    return await user_service.create_user(data)


@device_router.post("/user/all", response_model=typing.List[BaseUserSchema])
async def all_user(user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)]):
    users = await user_service.get_all()
    return users


@device_router.get("/user/{user_id}", response_model=BaseUserSchema)
async def user_me(user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)], user_id: UUID):
    user = await user_service.get_obj(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="user not found")


@device_router.get("/user/{user_id}/devices",
                   response_model=typing.List[BaseWebPushDeviceSchema | FCMDeviceSchema])
async def my_devices(user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)], user_id: UUID):
    user = await user_service.get_obj(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    fcm_device_service = BaseDeviceRepository(model=GCMDevice, create_schema=CreateDeviceSchema,
                                              user=user)
    web_push_device_service = BaseDeviceRepository(model=WebPushDevice, create_schema=CreateDeviceSchema,
                                                   user=user)
    fcm_device = await fcm_device_service.get_devices_by_user()
    web_push_device = await web_push_device_service.get_devices_by_user()
    return fcm_device + web_push_device


@device_router.patch("/user/{user_id}", response_model=BaseUserSchema)
async def update_user(user_id: str, user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)], data: UpdateUserSchema):
    return await user_service.update(user_id, data)


@device_router.post("/device/register",
                    response_model=typing.Union[BaseFCMDeviceSchema,
                    BaseWebPushDeviceSchema])
async def register_device(data: RegisterDeviceSchema, user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)]):
    user = await register_user(data=CreateUserSchema(id=data.user_id), user_service=user_service)
    data.device.user_id = data.user_id
    if data.device_type == TypeDevice.fcm:
        device_service = BaseDeviceRepository(model=GCMDevice,
                                              create_schema=FCMDeviceSchema,
                                              user=user)
        return await device_service.create(data=data.device)
    elif data.device_type == TypeDevice.webpush:
        device_service = BaseDeviceRepository(model=WebPushDevice,
                                              create_schema=WebPushDeviceSchema,
                                              user=user)
        return await device_service.create(data=data.device)
    else:
        raise HTTPException(status_code=400, detail="Invalid device_type")


@device_router.post("/user/{user_id}/send_message")
async def send_message(user_id: UUID, user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)], data: SendMessageSchema):
    devices: typing.List[GCMDevice | WebPushDevice] = await my_devices(user_service=user_service, user_id=user_id)
    print(devices)
    for device in devices:
        if isinstance(device, GCMDevice):
            service = GCMPushNotificationService(device=device)
        elif isinstance(device, WebPushDevice):
            service = WebPushNotificationService(device=device)
        else:
            continue
        result = await service.send_message(message=data.message)
        print(result.__dict__)
    return 'success'


@device_router.post("/user/{user_id}/send_message_by_type")
async def send_message_by_type(user_id: UUID, user_service: typing.Annotated[UserRepository,
Depends(get_user_repository)], data: SendMessageByTypeDeviceSchema):
    user = await user_service.get_obj(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if data.type_device == TypeDevice.fcm:
        fcm_device_service = BaseDeviceRepository(model=GCMDevice, create_schema=CreateDeviceSchema,
                                                  user=user)
        devices = await fcm_device_service.get_devices_by_user()
    elif data.type_device == TypeDevice.webpush:
        web_push_device_service = BaseDeviceRepository(model=WebPushDevice, create_schema=CreateDeviceSchema,
                                                       user=user)
        devices = await web_push_device_service.get_devices_by_user()
    else:
        raise HTTPException(status_code=400, detail="invalid type device")
    for device in devices:
        if isinstance(device, GCMDevice):
            service = GCMPushNotificationService(device=device)
        elif isinstance(device, WebPushDevice):
            service = WebPushNotificationService(device=device)
        else:
            continue
        await service.send_message(message=data.message)
    return 'success'
