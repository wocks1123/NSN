from fastapi import UploadFile
from sqlalchemy.orm import Session

from typing import List, Union

from app.common.utils import handle_file_upload
from app.crud.base import CRUDBase
from app.models import MediaFile
from app.schemas.MediaFile import MediaFileCreate, MediaFileUpdate


class CRUDMediaFile(CRUDBase[MediaFile, MediaFileCreate, MediaFileUpdate]):

    def create_with_file(self, db: Session, in_files: Union[UploadFile, List[UploadFile]]):
        files = handle_file_upload(in_files)
        objs = []
        for (saved_path, path, file_type) in files:
            objs.append(MediaFile(path=path, savedPath=saved_path, fileType=file_type))

        db.bulk_save_objects(objs)
        db.commit()
        return objs

    def get_by_path(self, db: Session, path: str):
        return db.query(MediaFile).filter(MediaFile.path == path).first()


media_file = CRUDMediaFile(MediaFile)
