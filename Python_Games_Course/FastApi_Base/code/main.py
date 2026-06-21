import contextlib

from fastapi import FastAPI

from code import api


@contextlib.asynccontextmanager
async def lifespan(_:FastAPI):
    #db.init()
    yield
    #db.close()


def init_app():
    app = FastAPI(
        title='collections',
        debug=False,
        version='0.0.1',
        docs_url='/docs',
        redoc_url='/redoc',
        lifespan=lifespan
    )

    app.include_router(api.router)

    return app


app = init_app()
