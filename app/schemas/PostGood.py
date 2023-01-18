from pydantic import BaseModel


class PostGoodBase(BaseModel):
    postId: int
    userId: str


class PostGoodCreate(PostGoodBase):
    ...


class PostGoodUpdate(PostGoodBase):
    ...
