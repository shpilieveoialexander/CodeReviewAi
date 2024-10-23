import json
from typing import Dict, List

import httpx
import openai
from fastapi import HTTPException, status

from core import settings
from utils.logger import logger


async def get_repo_contents(github_repo_url: str) -> List[Dict[str, str]]:
    headers = {
        "Authorization": f"token {settings.GIT_HUB_TOKEN}",
    }

    api_url = github_repo_url.replace(
        "https://github.com/", "https://api.github.com/repos/"
    )
    logger.info(f"Fetching repository contents from: {api_url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{api_url}/contents", headers=headers)
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting {api_url}: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub API is unavailable",
            )

        if response.status_code != 200:
            logger.warning(f"GitHub repository not found: {api_url}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="GitHub URL is not found or unavailable",
            )

        contents = response.json()
        logger.info(f"Retrieved {len(contents)} items from repository.")

        file_contents: List[Dict[str, str]] = []
        for item in contents:
            if item["type"] == "file" and item["name"].endswith(".py"):
                logger.info(f"Fetching file: {item['name']}")
                file_response = await client.get(item["download_url"], headers=headers)
                file_contents.append(
                    {"name": item["name"], "content": file_response.text}
                )

    logger.info(f"Successfully retrieved contents of {len(file_contents)} files.")
    return file_contents


async def generate_prompt(
    files: List[Dict[str, str]], role: str, assignment_description: str
) -> str:
    all_code_content = "\n\n".join([file["content"] for file in files])
    prompt = f"""
        You are a code reviewer. Analyze the following code:
        The code has been written by developers of varying levels {role}

        {all_code_content}

        Please provide your feedback in the following dictionary format:

        {{
            "comments": "Suggest areas where the code could be improved in terms of performance, maintainability, or clarity. It should be string",
            "downsides": "Highlight any issues, bugs, or mistakes found in the code. It should be string",
            "rating": "Based on the code, assess how the developer's level for his {role} for example "1/5", "5/5" etc(only rating without text)"
            "conclusion": "Conclusion about this developer with {role}",
        }}
        """
    logger.info(f"Generated prompt for {len(files)} files.")
    return prompt


async def generate_code_review(
    files: List[Dict[str, str]], role: str, assignment_description: str
) -> str:
    openai.api_key = settings.OPEN_AI_API_KEY
    logger.info("Starting to generate code review.")
    file_names = [file["name"] for file in files]
    prompt: str = await generate_prompt(files, role, assignment_description)
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    logger.info("Code review generation completed successfully.")
    feedback = response.choices[0].message.content.strip()

    review_code = feedback.strip("```json\n").strip()
    review_code = json.loads(review_code)

    review_code["assignment_description"] = assignment_description
    review_code["filenames"] = file_names
    return review_code
