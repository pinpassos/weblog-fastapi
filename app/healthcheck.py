from http import HTTPStatus

from fastapi import APIRouter

healthcheck_router = APIRouter()


@healthcheck_router.get(path="", name="Health check endpoint")
def healthcheck():
    """Check the API status."""
    return {"status": HTTPStatus.OK}
