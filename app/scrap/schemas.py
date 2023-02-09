from datetime import datetime

from app.models import NSNBase


class ScrapBase(NSNBase):
    user_id: str
    post_id: int


class ScrapCreate(ScrapBase):
    ...


class ScrapDelete(ScrapBase):
    ...


class ScrapResponse(ScrapBase):
    created_at: datetime
