import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.core import get_db

from .service import get_by_path


media_router = APIRouter()


@media_router.get('/{identifier}')
def get_image(identifier: str, db_session: Session = Depends(get_db)):
    file = get_by_path(db_session=db_session, identifier=identifier)
    return FileResponse(os.path.join(file.saved_path))
