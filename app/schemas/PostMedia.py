from pydantic import BaseModel


class PostMediaBase(BaseModel):
    path: str
    mediaType: str


class PostMediaCreate(PostMediaBase):
    postId: int


class PostMediaUpdate(PostMediaBase):
    ...


class PostMediaInPost(PostMediaBase):

    class Config:
        orm_mode = True
