from fastapi.encoders import jsonable_encoder

from typing import List

from app.crud.base import CRUDBase
from app.models import PostMedia
from app.schemas.PostMedia import PostMediaCreate, PostMediaUpdate


class CRUDPostMedia(CRUDBase[PostMedia, PostMediaCreate, PostMediaUpdate]):

    def create_bulk(self, db, create_schemes: List[PostMediaCreate]):
        objs = []
        for s in create_schemes:
            obj_in_data = jsonable_encoder(s)
            db_obj = self.model(**obj_in_data)  # type: ignore
            objs.append(db_obj)

        db.bulk_save_objects(objs)
        db.commit()
        return objs


post_media = CRUDPostMedia(PostMedia)
