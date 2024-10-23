import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app

from .utils import fake

base_url = "http://test"
endpoint_url = "/api/v1/review/"


@pytest.mark.asyncio
async def test_sucsess_review_code():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            endpoint_url,
            json={
                "repo_url": "https://github.com/shekhargulati/python-flask-docker-hello-world",
                "candidate_level": "junior",
                "assignment_description": fake.sentence(),
            },
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_invalid_review_code_not_valid_string_url():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            endpoint_url,
            json={
                "repo_url": fake.url(),
                "candidate_level": "junior",
                "assignment_description": fake.sentence(),
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_invalid_review_code_without_candidate_level():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            endpoint_url,
            json={
                "repo_url": "https://github.com/shekhargulati/python-flask-docker-hello-world",
                "assignment_description": fake.sentence(),
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
