from fastapi import APIRouter, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from repo.review import generate_code_review, get_repo_contents
from schemas import v1 as schemas_v1
from utils.redis import redis_cache

router = APIRouter()

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas_v1.ReviewResponse
)
@redis_cache("code_review")
@limiter.limit("10/minute")
async def review_code(
    request: Request, input_data: schemas_v1.Review
) -> schemas_v1.ReviewResponse:
    """
    Generate a code review based on the contents of a GitHub repository.

    - **repo_url**: URL of the GitHub repository.
    - **candidate_level**: The level of the candidate (e.g., junior, mid-level, senior).
    - **assignment_description**: Description of the assignment.

    Returns structured feedback containing comments, downsides, rating, conclusion,
    along with the assignment description and filenames analyzed.
    """
    files = await get_repo_contents(input_data.repo_url)
    review = await generate_code_review(
        files, input_data.candidate_level, input_data.assignment_description
    )
    return review
