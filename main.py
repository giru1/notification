import os

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from endpoints.device import device_router

app = FastAPI()

endpoints_routers = [device_router]
for router in endpoints_routers:
    app.include_router(router)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.getenv('NOTIFICATION_SERVICE_PORT')),
                log_level=os.getenv('LOG_LEVEL').lower(), reload=True)
