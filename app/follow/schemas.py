from app.core.enums import FollowType
from app.models import NSNBase

from app.auth.schemas import UserCardResponse


class FollowBase(NSNBase):
    from_user_id: str
    to_user_id: str


class FollowCreate(FollowBase):
    follow_type: FollowType


class FollowRead(FollowBase):
    ...


class FollowDelete(FollowBase):
    ...


class FollowResponse(FollowBase):
    follow_type: FollowType


class FollowerResponse(FollowBase):
    follow_type: FollowType
    from_user: UserCardResponse
    followed: bool


class FollowingResponse(FollowBase):
    follow_type: FollowType
    to_user: UserCardResponse



