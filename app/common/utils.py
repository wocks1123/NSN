from fastapi import UploadFile

import uuid
import os
from typing import List, Union

from app.common.consts import SERVER_IMG_DIR


def get_filetype(ext):
    IMAGE = ['jpg', 'jpeg', 'png', 'gif']
    VIDEO = ['avi', 'mp4']

    if ext in IMAGE:
        return 'image'
    elif ext in VIDEO:
        return 'video'
    else:
        return 'etc'


def handle_file_upload(in_file: Union[UploadFile, List[UploadFile]]):
    files = in_file if isinstance(in_file, List) else [in_file]

    ret = [] # [(saved_path, path, file_type), ...]
    for file in files:
        _, extension = os.path.splitext(file.filename)
        file_type = get_filetype(extension)
        file_id = uuid.uuid4().hex
        file_name = f'{file_id}{extension}'
        saved_path = os.path.join(SERVER_IMG_DIR, file_name)
        with open(saved_path, "wb+") as file_object:
            file_object.write(file.file.read())

        ret.append((saved_path, file_id, file_type))

    return ret
