import uvicorn

from api.core.config import Settings
from api.core.factory import create_app

settings = Settings()
app = create_app(settings)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.service_host, port=settings.service_port, reload=settings.debug)
