from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base

post_category_association = Table(
    "post_category", Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(String(150), unique=True)
    author = relationship("User", back_populates="posts")
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    categories: Mapped[List["Category"]] = relationship(back_populates="posts", secondary=post_category_association)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    posts: Mapped[List["Post"]] = relationship(back_populates="categories", secondary=post_category_association)
