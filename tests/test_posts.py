import pytest
from sqlalchemy.exc import IntegrityError

from app.posts.models import Category, Post
from app.users.models import User


def test_create_new_post(session, user, post):
    """Ensure post can be createad."""
    post.author = user

    session.add(post)
    session.commit()
    session.refresh(post)

    assert post.id == 1
    assert post.author_id == 1
    assert isinstance(post.slug, str)
    assert isinstance(post.content, str)
    assert isinstance(post.summary, str)
    assert isinstance(post.author, User)
    assert isinstance(post.categories, list)


def test_create_new_category(session, category):
    """Ensure category can be createad."""
    session.add(category)
    session.commit()
    session.refresh(category)

    assert category.id == 1
    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.is_active, bool)
    assert isinstance(category.posts, list)


def test_if_category_has_unique_constraint(session, category, duplicated_category):
    """Ensure that there is only one category per name."""
    session.add_all([category, duplicated_category])
    with pytest.raises(IntegrityError):
        session.commit()


def test_associate_category_to_post(session, user, category, post):
    """Ensure that category can be associated with a post."""
    post.author = user
    post.categories = [category]

    session.add(post)
    session.commit()

    assert len(post.categories) == 1
    assert isinstance(post.categories[0], Category)


def test_associate_post_to_user(session, user, post):
    """Ensure that post can be associated with a user."""
    user.posts = [post]
    session.add(user)
    session.commit()

    assert len(user.posts) == 1
    assert isinstance(user.posts[0], Post)


def test_author_required_for_post_creation(session, post):
    """Ensure that a post cannot be created without an author."""
    session.add(post)
    with pytest.raises(IntegrityError):
        session.commit()
