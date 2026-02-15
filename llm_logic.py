import os
from anthropic import Anthropic

api_key = os.environ.get("ANTHROPIC_API_KEY")


import json
def pick_most_relevant_result(text_original_message: str, parsed_result_list: list):
    """
    Format-agnostic version.
    Accepts:
        - list of (title, url)
        - list of (title, description, url)
        - list of dicts
    Returns:
        string formatted like previously: "('title', 'url')"
    """

    client = Anthropic(api_key=api_key)

    # I use the same logic for the LLM to pick the most relevant result, be it in a list of scraped articles, or a list of jira issues.
    normalized = []

    for item in parsed_result_list:
        if isinstance(item, dict):
            title = item.get("summary") or item.get("title") or ""
            description = item.get("description", "")
            url = item.get("ticket_url") or item.get("url") or ""

        elif isinstance(item, tuple):
            if len(item) == 2:
                title, url = item
                description = ""
            elif len(item) == 3:
                title, description, url = item
            else:
                continue
        else:
            continue

        normalized.append({
            "title": title,
            "description": description,
            "url": url
        })

    # ---- Format prompt ----
    formatted_options = "\n".join(
        f'{i}. Title: "{item["title"]}" | Description: "{item["description"]}" | URL: {item["url"]}'
        for i, item in enumerate(normalized)
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

Respond with ONLY a JSON object in this exact format:
{{"index": <number>, "title": "<title>", "url": "<url>"}}
"""
            }
        ]
    )

    response_text = message.content[0].text.strip()

    # JSON parsing
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            # fallback to first result
            result = {
                "title": normalized[0]["title"],
                "url": normalized[0]["url"]
            }

    # ---- SAME RETURN FORMAT AS BEFORE ----
    search_result = f'<{result["url"]}|{result["title"]}>'
    return search_result

def generate_structured_issue(text_original_message):
    client = Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""
Turn the following user problem into a structured Jira issue.

User message:
"{text_original_message}"

Respond ONLY with JSON:
{{
  "summary": "...",
  "description": "..."
}}
"""
            }
        ]
    )

    import json
    import re

    response_text = message.content[0].text.strip()

    try:
        return json.loads(response_text)
    except:
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        return json.loads(match.group())
