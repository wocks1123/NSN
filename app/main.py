import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings
from app.db import Base, engine

from app.router import api_router as api


Base.metadata.create_all(bind=engine)



async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )

exception_handlers = {404: not_found}


def create_app():
    app = FastAPI(
        exception_handlers=exception_handlers
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def de_session_middleware(request: Request, call_next):
        try:
            session = scoped_session(
                sessionmaker(
                    autocommit=settings.AUTO_COMMIT,
                    autoflush=False,
                    bind=engine
                )
            )
            request.state.db = session()
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            request.state.db.close()
        return response

    # add routers...
    app.include_router(api)


    return app


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

