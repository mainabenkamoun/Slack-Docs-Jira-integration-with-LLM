import os
from anthropic import Anthropic

api_key = os.environ.get("ANTHROPIC_API_KEY")


import json
def pick_most_relevant_result(text_original_message: str, parsed_result_list: list[tuple[str, str]]) -> tuple[str, str]:
    """
    Uses Claude to pick the most relevant (title, url) from parsed_result_list
    based on the user's query.
    """
    client = Anthropic(api_key=api_key)

    # Format the list for the prompt
    formatted_options = "\n".join(
        f'{i}. Title: "{title}" | URL: {url}'
        for i, (title, url) in enumerate(parsed_result_list)
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"""Given the following user query and a list of article options, pick the single most relevant article.

User query: "{text_original_message}"

Available articles:
{formatted_options}

Respond with ONLY a JSON object in this exact format (no other text):
{{"index": <number>, "title": "<title>", "url": "<url>"}}
"""
            }
        ]
    )

    # Parse the response
    response_text = message.content[0].text.strip()
    result = json.loads(response_text)
    search_result = f'{result["title"], result["url"]}'
    return search_result
    

