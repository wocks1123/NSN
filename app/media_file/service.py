import uuid
import os
from typing import List, Union, Optional

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings

from .models import MediaFile

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50   # 50MB


def get_filetype(ext):
    IMAGE = ['jpg', 'jpeg', 'png', 'gif']
    VIDEO = ['avi', 'mp4']

    if ext in IMAGE:
        return 'image'
    elif ext in VIDEO:
        return 'video'
    else:
        return 'etc'


async def handle_file_upload(
    db_session: Session, in_file: Union[UploadFile, List[UploadFile]]
) -> Union[MediaFile, List[MediaFile]]:
    files = in_file if isinstance(in_file, List) else [in_file]

    objs = [] # [(saved_path, path, file_type), ...]
    for file in files:
        _, extension = os.path.splitext(file.filename)
        file_type = get_filetype(extension)
        file_id = uuid.uuid4().hex
        file_name = f'{file_id}{extension}'
        saved_path = os.path.join(settings.MEDIA_ROOT_PATH, file_name)
        async with aiofiles.open(saved_path, "wb+") as f:
            while chunk := await file.read(DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

        objs.append(
            MediaFile(
                identifier=file_id,
                saved_path=saved_path,
                file_type=file_type
            )
        )

    db_session.bulk_save_objects(objs)
    db_session.commit()
    return objs if len(objs) > 1 else objs[0]


def get_by_path(*, db_session, identifier: str) -> Optional[MediaFile]:
    return db_session.query(MediaFile).filter(MediaFile.identifier == identifier).one_or_none()
