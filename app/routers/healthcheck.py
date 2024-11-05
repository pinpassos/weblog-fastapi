from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter()


@router.get(path="", name="Health check endpoint")
def healthcheck():
    """Check the API status."""
    return {"status": HTTPStatus.OK}
