import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import router as users_router

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

    # add routers...
    app.include_router(users_router, tags=["users"])

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
