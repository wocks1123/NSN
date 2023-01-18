from pydantic import BaseModel


class MediaFileBase(BaseModel):
    path: str
    saved_path: str
    fileType: str


class MediaFileCreate(MediaFileBase):
    ...


class MediaFileUpdate(MediaFileBase):
    ...


class MediaFileScheme(BaseModel):
    class Config:
        orm_mode = True
