import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import router as users_router
from app.db import Base, engine

from app.models.ModelBase import Base
from app.database import engine


Base.metadata.create_all(bind=engine)

def create_app():
    app = FastAPI()

    # db initialize...
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        # allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # redis initialize...

    # middleware initialize...
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
    app.include_router(users_router, tags=["users"])

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
