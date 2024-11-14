from typing import List, Optional

from pydantic import BaseModel

from app.users.schemas import UserRead


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool


class CreateCategorySchema(BaseModel):
    name: str
    description: str
    is_active: Optional[bool]


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PostSchema(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    slug: str
    author: UserRead
    categories: List[CategorySchema]


class CreatePostSchema(BaseModel):
    title: str
    summary: str
    content: str
    slug: str
    categories: List[CategorySchema]


class UpdatePostSchema(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    categories: List[CategorySchema]
