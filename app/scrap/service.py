from sqlalchemy.orm import Session

from .models import Scrap
from .schemas import (
    ScrapCreate,
    ScrapDelete,
)


def create(
    *,
    db_session: Session,
    scrap_in: ScrapCreate,
) -> Scrap:
    scrap = Scrap(
        **scrap_in.dict()
    )
    db_session.add(scrap)
    db_session.commit()
    db_session.refresh(scrap)
    return scrap


def delete(
    *,
    db_session: Session,
    scrap_in: ScrapDelete,
) -> Scrap:
    scrap = db_session.query(Scrap)\
        .filter(
            Scrap.user_id == scrap_in.user_id,
            Scrap.post_id == scrap_in.post_id
        ).one_or_none()
    db_session.delete(scrap)
    db_session.commit()
    return scrap
