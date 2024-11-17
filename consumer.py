import asyncio
import json

import aio_pika

from config.config import settings
from models.user import User, GCMDevice, WebPushDevice
from schemas.device import CreateDeviceSchema
from schemas.register_device import TypeDevice
from schemas.send_message import SendMessageByDeviceRabbitSchema
from schemas.user import CreateUserSchema
from services.base import BaseDeviceRepository
from services.gcm_service import GCMPushNotificationService
from services.user import UserRepository
from services.webpush_service import WebPushNotificationService


async def send_message_from_rabbit(message: SendMessageByDeviceRabbitSchema):
    user_service = UserRepository(model=User, create_schema=CreateUserSchema)
    user = await user_service.get_obj(message.user_id)
    if not user:
        # Need process with?
        return
    fcm_device_service = BaseDeviceRepository(model=GCMDevice, create_schema=CreateDeviceSchema,
                                                  user=user)
    fcm_device = await fcm_device_service.get_devices_by_user()
    web_push_device_service = BaseDeviceRepository(model=WebPushDevice, create_schema=CreateDeviceSchema,
                                                   user=user)
    web_push_device = await web_push_device_service.get_devices_by_user()
    devices = fcm_device + web_push_device
    for device in devices:
        if isinstance(device, GCMDevice):
            service = GCMPushNotificationService(device=device)
        elif isinstance(device, WebPushDevice):
            service = WebPushNotificationService(device=device)
        else:
            continue
        await service.send_message(message=message.message)
    return 'success'


async def process_message(
        message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        message = json.loads(message.body.decode('utf-8'))
        data_message = SendMessageByDeviceRabbitSchema.model_validate(message)
        await send_message_from_rabbit(data_message)


async def main() -> None:
    connection = await aio_pika.connect_robust(
        settings.rabbit_con_url,
    )

    queue_name = settings.rabbit_queue_name

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=False)

    await queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    except Exception as e:
        print(e)
    finally:
        await connection.close()


if __name__ == "__main__":
    print('start consumer loop')
    asyncio.run(main())
