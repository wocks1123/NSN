from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.core import get_db

from .schemas import (
    FollowRead,
    FollowCreate,
    FollowDelete,
    FollowResponse,
    FollowerResponse,
    FollowingResponse
)
from .service import (
    create,
    get,
    get_from_user_by_user_id,
    get_to_user_by_user_id,
    update,
    delete
)


follow_router = APIRouter()


@follow_router.post("/", response_model=FollowResponse)
def create_follow(
    follow_in: FollowCreate,
    db_session: Session = Depends(get_db)
):
    return create(db_session=db_session, follow_in=follow_in)


@follow_router.get("/", response_model=FollowResponse)
def read_follow(
    follow_in: FollowRead,
    db_session: Session = Depends(get_db)
):
    return get(db_session=db_session, follow_in=follow_in)


@follow_router.put("/", response_model=FollowResponse)
def update_follow(
    follow_in: FollowRead,
    db_session: Session = Depends(get_db)
):
    follow = get(db_session=db_session, follow_in=follow_in)
    return update(db_session=db_session, follow=follow, follow_in=follow_in)


@follow_router.delete("/", response_model=FollowResponse)
def delete_follow(
    follow_in: FollowDelete,
    db_session: Session = Depends(get_db)
):
    return delete(db_session=db_session, follow_in=follow_in)


@follow_router.get("/from", response_model=List[FollowingResponse])
def get_following(user_id: str, db_session: Session = Depends(get_db)):
    ret = get_from_user_by_user_id(db_session=db_session, user_id=user_id)
    return ret


@follow_router.get("/to", response_model=List[FollowerResponse])
def get_follower(user_id: str, db_session: Session = Depends(get_db)):
    followers = get_to_user_by_user_id(db_session=db_session, user_id=user_id)
    for f in followers:
        f.followed = bool(get(db_session=db_session, follow_in=FollowRead(from_user_id=user_id, to_user_id=f.from_user_id)))
    return followers
