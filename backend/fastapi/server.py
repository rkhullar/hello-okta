import uvicorn

from config import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from okta_flow import OktaAuthCodeBearer
from router import router


def link_okta(app: FastAPI, settings: Settings = None) -> OktaAuthCodeBearer:
    settings = settings or app.extra.get('settings')
    okta_client = OktaAuthCodeBearer(domain=settings.okta_domain)
    app.extra['okta_flow'] = okta_client
    return okta_client


def init_cors(app: FastAPI, settings: Settings = None):
    settings = settings or app.extra.get('settings')
    app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=False,
                       allow_methods=['*'], allow_headers=['*'])


def create_app(settings: Settings, test: bool = False) -> FastAPI:
    app = FastAPI(
        settings=settings,
        swagger_ui_init_oauth={
            'clientId': settings.okta_client_id,
            'usePkceWithAuthorizationCodeGrant': True,
            'scopes': ' '.join(['openid', 'profile', 'email'])
        }
    )

    app.include_router(router)
    if not test:
        # link_okta(app)
        init_cors(app)
    return app


settings = Settings()
app = create_app(settings)

if __name__ == '__main__':
    uvicorn.run('server:app', host=settings.service_host, port=settings.service_port, reload=settings.debug)
