import warnings

from pywebpush import webpush, WebPushException

from config.config import settings
from db.session import async_session_maker
from exceptions.exception import WebPushError
from models.user import WebPushDevice
from schemas.web_push import WebPushResultSchema
from services.base import BaseDeviceRepository


class WebPushService(BaseDeviceRepository):
    pass


class WebPushNotificationService:
    def __init__(self, device: WebPushDevice):
        self.device = device

    async def get_subscription_info(self):
        if self.device.registration_id.startswith("https://"):
            endpoint = self.device.registration_id
        else:
            url = settings.push_settings.get_wp_post_url(self.device.browser.value)
            endpoint = "{}/{}".format(url, self.device.registration_id)
            warnings.warn(
                "registration_id should be the full endpoint returned from pushManager.subscribe",
                DeprecationWarning,
                stacklevel=2,
            )
        return {
            "endpoint": endpoint,
            "keys": {
                "auth": self.device.auth,
                "p256dh": self.device.p256dh,
            }
        }

    async def deactivate_device(self):
        async with async_session_maker() as session:
            self.device.active = False
            await session.commit()

    async def webpush_send_message(self, message, **kwargs) -> WebPushResultSchema:
        subscription_info = await self.get_subscription_info()
        try:
            response = webpush(
                subscription_info=subscription_info,
                data=message,
                vapid_private_key=settings.push_settings.wp_private_key,
                vapid_claims=settings.push_settings.wp_claims,
                **kwargs
            )
            if response.ok:
                return WebPushResultSchema(original_registration_id=self.device.registration_id,
                                           success=True)
            return WebPushResultSchema(original_registration_id=self.device.registration_id,
                                       success=False, error_message=response.content)
        except WebPushException as e:
            if e.response is not None and e.response.status_code in [404, 410]:
                await self.deactivate_device()
                return WebPushResultSchema(original_registration_id=self.device.registration_id,
                                           success=False, error_message=e.message)
            raise WebPushError(e.message)
