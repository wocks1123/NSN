from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .models import Follow
from .schemas import (
    FollowRead,
    FollowCreate,
    FollowDelete,
)


def create(
    *,
    db_session: Session,
    follow_in: FollowCreate,
) -> Follow:
    post_like = Follow(
        **follow_in.dict()
    )
    db_session.add(post_like)
    db_session.commit()
    db_session.refresh(post_like)
    return post_like


def get(
    *,
    db_session: Session,
    follow_in: FollowRead
) -> Optional[Follow]:
    return db_session.query(Follow)\
        .filter(Follow.from_user_id == follow_in.from_user_id) \
        .filter(Follow.to_user_id == follow_in.to_user_id) \
        .one_or_none()


def get_from_user_by_user_id(
    *,
    db_session: Session,
    user_id: str
) -> List[Follow]:
    return db_session.query(Follow) \
        .filter(Follow.from_user_id == user_id) \
        .all()


def get_to_user_by_user_id(
    *,
    db_session: Session,
    user_id: str
):
    return db_session.query(Follow) \
        .filter(Follow.to_user_id == user_id) \
        .all()


def update(
    *,
    db_session: Session,
    follow: Follow,
    follow_in: FollowRead,
) -> Follow:
    follow_data = jsonable_encoder(follow)
    update_data = follow_in.dict(exclude_unset=True)
    for field in follow_data:
        if field in update_data:
            setattr(follow, field, update_data[field])

    db_session.add(follow)
    db_session.commit()
    db_session.refresh(follow)
    return follow


def delete(
    *,
    db_session: Session,
    follow_in: FollowDelete,
) -> Follow:
    follow = db_session.query(Follow)\
        .filter(
            Follow.from_user_id == follow_in.from_user_id,
            Follow.to_user_id == follow_in.to_user_id
        ).one_or_none()
    db_session.delete(follow)
    db_session.commit()
    return follow
