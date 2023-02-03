from app.models import NSNBase


class PostLikeBase(NSNBase):
    post_id: int
    user_id: str


class PostLikeCreate(PostLikeBase):
    ...


class PostLikeDelete(PostLikeBase):
    ...


class PostLikeRead(PostLikeBase):
    ...


class CommentLikeBase(NSNBase):
    comment_id: int
    user_id: str


class CommentLikeCreate(CommentLikeBase):
    ...


class CommentLikeDelete(CommentLikeBase):
    ...


class CommentLikeRead(CommentLikeBase):
    ...
