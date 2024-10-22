from typing import List

from pydantic import BaseModel, validator

from .constants import Candidate


class Review(BaseModel):
    assignment_description: str
    repo_url: str
    candidate_level: Candidate

    @validator("repo_url")
    def validate_github_url(cls, v):
        if not v.startswith("https://github.com/"):
            raise ValueError('URL must start with "https://github.com/"')
        return v


class ReviewResponse(BaseModel):
    assignment_description: str
    filenames: List[str]
    comments: str
    downsides: str
    rating: str
    conclusion: str
