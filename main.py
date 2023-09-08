from fastapi import FastAPI

from logging_conf import LoggerSingleton
from database import Base, engine
from loguru import logger

from routes.auth import router as auth_router
from routes.sim import router as sim_router
from routes.users import router as user_router

logger_setup = LoggerSingleton()


app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(sim_router, prefix="/sim", tags=["sim"])
app.include_router(user_router, prefix="/user", tags=["users"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
