import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.db.db import Base, engine, AsyncSessionLocal
from app.routes import all_routes


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield
    await engine.dispose()



def get_app():
    fastapi_app = FastAPI(lifespan=lifespan)

    @fastapi_app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        async with AsyncSessionLocal() as session:
            request.state.db = session
            response = await call_next(request)
        return response

    fastapi_app.include_router(all_routes)
    return fastapi_app

app = get_app()


if __name__ == "__main__":
    from app.core.conf import settings
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True)
