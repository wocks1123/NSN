from fastapi import APIRouter

from app.auth.views import user_router, auth_router
from app.comment.views import comment_router
from app.follow.views import follow_router
from app.like.views import like_router
from app.media_file.views import media_router
from app.post.views import post_router
from app.scrap.views import scrap_router


api_router = APIRouter()


api_router.include_router(user_router, prefix="/users", tags=["user"])
api_router.include_router(auth_router, prefix="", tags=["auth"])
api_router.include_router(comment_router, prefix="/comments", tags=["comment"])
api_router.include_router(follow_router, prefix="/follows", tags=["follow"])
api_router.include_router(like_router, prefix="/likes", tags=["like"])
api_router.include_router(media_router, prefix="/media", tags=["media"])
api_router.include_router(post_router, prefix="/posts", tags=["post"])
api_router.include_router(scrap_router, prefix="/scraps", tags=["scrap"])
