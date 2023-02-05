from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.core import get_db

from .schemas import (
    ScrapCreate,
    ScrapDelete,
    ScrapResponse
)
from .service import (
    create,
    delete
)


scrap_router = APIRouter()


@scrap_router.post("/", response_model=ScrapResponse)
def create_scrap(
    scrap_in: ScrapCreate,
    db_session: Session = Depends(get_db)
):
    return create(db_session=db_session, scrap_in=scrap_in)


@scrap_router.delete("/", response_model=ScrapResponse)
def delete_scrap(
    scrap_in: ScrapDelete,
    db_session: Session = Depends(get_db)
):
    return delete(db_session=db_session, scrap_in=scrap_in)
