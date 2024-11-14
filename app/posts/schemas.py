from app.users.schemas import UserRead
from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    slug: str
    author: UserRead
    categories: list | None = []  # TODO: Change to Category schema


class CreatePostSchema(BaseModel):
    title: str
    summary: str
    content: str
    slug: str
    categories: list | None = []  # TODO: Change to Category schema


class UpdatePostSchema(BaseModel):
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    slug: str | None = None
    categories: list | None = []  # TODO: Change to Category schema
