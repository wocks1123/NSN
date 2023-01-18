from pydantic import BaseModel


class CommentGoodBase(BaseModel):
    postId: int
    userId: str


class CommentGoodCreate(CommentGoodBase):
    ...


class CommentGoodUpdate(CommentGoodBase):
    ...
