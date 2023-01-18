from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import CommentGood, PostGood
from app.schemas.CommentGood import CommentGoodCreate, CommentGoodUpdate
from app.schemas.PostGood import PostGoodCreate, PostGoodUpdate


class CRUDCommentGood(CRUDBase[CommentGood, CommentGoodCreate, CommentGoodUpdate]):
    ...


class CRUDPostGood(CRUDBase[PostGood, PostGoodCreate, PostGoodUpdate]):
    ...


comment_good = CRUDCommentGood(CommentGood)
post_good = CRUDPostGood(PostGood)
