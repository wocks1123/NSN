from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import os

from app import crud
from app.deps import get_db


router = APIRouter(prefix="/files")


@router.get('/{path}')
def get_image(path: str, db: Session = Depends(get_db)):
    file = crud.media_file.get_by_path(db, path=path)
    return FileResponse(os.path.join(file.savedPath))
