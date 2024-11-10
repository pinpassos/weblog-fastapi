from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError


def test_create_new_user(session, user):
    """Ensure user can be createad."""
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id == 1
    assert isinstance(user.username, str)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert isinstance(user.posts, list)


def test_if_user_has_unique_constraint(session, user, duplicated_user):
    """Ensure that there is only one user per username"""
    session.add_all([user, duplicated_user])
    with pytest.raises(IntegrityError):
        session.commit()
