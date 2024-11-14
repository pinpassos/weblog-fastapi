from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.posts.models import Post
from app.posts.schemas import CreatePostSchema, PostSchema, UpdatePostSchema
from app.settings.database import async_session
from app.users.manager import current_active_user
from app.users.models import User

post_router = APIRouter()
SessionAsync = Annotated[AsyncSession, Depends(async_session)]
CurrentUser = Annotated[User, Depends(current_active_user)]


@post_router.get(path="/", tags=["posts"], response_model=List[PostSchema])
async def get_all_posts(session: SessionAsync):

    select_all_posts = await session.execute(
        select(Post)
    )
    return select_all_posts.scalars().all()


@post_router.get(path="/{post_id}", tags=["posts"], response_model=PostSchema)
async def get_post(post_id: int, session: SessionAsync):

    get_post = await session.execute(
        select(Post).where(Post.id == post_id)
    )

    post = get_post.scalar()

    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Post not found"
        )

    return post


@post_router.post(path="/", tags=["posts"], response_model=PostSchema)
async def create_post(user: CurrentUser, post: CreatePostSchema, session: SessionAsync):

    new_post = Post(
        title=post.title,
        summary=post.summary,
        content=post.content,
        slug=post.slug,
        author=user,
        categories=post.categories,
    )

    try:
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    else:
        return new_post


@post_router.patch(path="/{post_id}", tags=["posts"], response_model=PostSchema)
async def update_post(user: CurrentUser, post_id: int, post_data: UpdatePostSchema, session: SessionAsync):

    data_to_update = post_data.model_dump(exclude_unset=True)
    if not data_to_update:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="At least one valid field must be provided for update"
        )

    get_post = await session.execute(
        select(Post).where(Post.id == post_id)
    )
    post = get_post.scalar()

    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Post not found"
        )

    for key, value in data_to_update.items():
        setattr(post, key, value)

    try:
        session.add(post)
        await session.commit()
        await session.refresh(post)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    else:
        return post


@post_router.delete(path="/{post_id}", tags=["posts"], response_model=int)
async def delete_post(user: CurrentUser, post_id: int, session: SessionAsync):

    get_post = await session.execute(
        select(Post).where(Post.id == post_id)
    )
    post = get_post.scalar()

    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Post not found"
        )

    try:
        await session.delete(post)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    else:
        return f"Post {post_id} has been deleted"


# @post_router.get(path="", description="Get all categories")
# def get_all_categories():
#     pass


# @post_router.get(path="", description="Get category")
# def get_category():
#     pass


# @post_router.post(description="Create new category")
# def create_category():
#     pass


# @post_router.patch(description="Update category")
# def update_category():
#     pass


# @post_router.delete(description="Delete category")
# def delete_category():
#     pass
