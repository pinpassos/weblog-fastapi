from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.posts.models import Category, Post
from app.posts.schemas import (CategorySchema, CreateCategorySchema,
                               CreatePostSchema, PostSchema,
                               UpdateCategorySchema, UpdatePostSchema)
from app.settings.database import async_session
from app.users.manager import current_active_user
from app.users.models import User

post_router = APIRouter()
categories_router = APIRouter()
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


@post_router.delete(path="/{post_id}", tags=["posts"], response_model=str)
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


@categories_router.get(path="/", tags=["categories"], response_model=List[CategorySchema])
async def get_all_categories(user: CurrentUser, session: SessionAsync):
    get_categories = await session.execute(
        select(Category)
    )
    return get_categories.scalars().all()


@categories_router.get(path="/{category_id}", tags=["categories"], response_model=CategorySchema)
async def get_category(user: CurrentUser, category_id: int, session: SessionAsync):
    get_category = await session.execute(
        select(Category).where(Category.id == category_id)
    )

    category = get_category.scalar()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Category not found"
        )

    return category


@categories_router.post(path="/", tags=["categories"], response_model=CategorySchema)
async def create_category(user: CurrentUser, category: CreateCategorySchema, session: SessionAsync):
    category_to_create = Category(
        name=category.name,
        description=category.description,
        is_active=category.is_active
    )

    try:
        session.add(category_to_create)
        await session.commit()
        await session.refresh(category_to_create)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    else:
        return category_to_create


@categories_router.patch(path="/{category_id}", tags=["categories"], response_model=CategorySchema)
async def update_category(user: CurrentUser, category_id: int, category_data: UpdateCategorySchema, session: SessionAsync):

    data_to_update = category_data.model_dump(exclude_unset=True)
    if not data_to_update:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="At least one valid field must be provided for update"
        )

    get_category = await session.execute(
        select(Category).where(Category.id == category_id)
    )

    category = get_category.scalar()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Category not found"
        )

    for key, value in data_to_update.items():
        setattr(category, key, value)

    try:
        session.add(category)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    else:
        return category


@categories_router.delete(path="/{category_id}", tags=["categories"], response_model=str)
async def delete_category(user: CurrentUser, category_id: int, session: SessionAsync):
    get_category = await session.execute(
        select(Category).where(Category.id == category_id)
    )

    category = get_category.scalar()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Category not found"
        )

    try:
        await session.delete(category)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    else:
        return f"Category {category_id} has been deleted"
