import uvicorn
from fastapi import FastAPI

from config import Settings
from okta import OktaClient
from router import router


def link_okta(app: FastAPI, settings: Settings = None) -> OktaClient:
    settings = settings or app.extra.get('settings')
    okta_client = OktaClient(domain=settings.okta_domain, client_id=settings.okta_client_id,
                             client_secret=settings.okta_client_secret)
    app.extra['okta_client'] = okta_client
    return okta_client


def create_app(settings: Settings, test: bool = False) -> FastAPI:
    app = FastAPI(settings=settings)
    app.include_router(router)
    if not test:
        link_okta(app)
    return app


settings = Settings()
app = create_app(settings)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.service_host, port=settings.service_port, reload=settings.debug)
