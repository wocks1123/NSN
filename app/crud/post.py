from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.Post import Post
from app.schemas.Post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):

    def get_multi_date_desc(
        self, db: Session, *, cursor: int
    ):
        if cursor == 0:
            return db.query(Post) \
                .order_by(Post.created_at.desc()) \
                .limit(3).all()

        else:
            return db.query(Post)\
                    .order_by(Post.created_at.desc())\
                    .filter(Post.id < cursor)\
                    .limit(3).all()


post = CRUDPost(Post)
