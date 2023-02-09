from sqlalchemy import (
    Column, String, Enum, ForeignKey
)
from sqlalchemy.orm import relationship

from app.core.enums import FollowType
from app.db import Base


class Follow(Base):
    from_user_id = Column(String(32), ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    to_user_id = Column(String(32), ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    follow_type = Column(Enum(FollowType), nullable=False, default=FollowType.ACCEPT)

    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])
