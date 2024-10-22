from fastapi import APIRouter, status

from repo.review import generate_code_review, get_repo_contents
from schemas import v1 as schemas_v1

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas_v1.ReviewResponse
)
async def review_code(input_data: schemas_v1.Review) -> schemas_v1.ReviewResponse:
    """
    Generate a code review based on the contents of a GitHub repository.

    - **repo_url**: URL of the GitHub repository.
    - **candidate_level**: The level of the candidate (e.g., junior, mid-level, senior).
    - **assignment_description**: Description of the assignment.

    Returns a structured feedback containing comments, downsides, rating, conclusion,
    along with the assignment description and filenames analyzed.
    """
    files = await get_repo_contents(input_data.repo_url)
    review = await generate_code_review(
        files, input_data.candidate_level, input_data.assignment_description
    )
    return review
