import requests
import os
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
import json
# ----------------------------
# Set environment variables directly or via os.environ

#ID d'organisation: 
#61074f23-ecd7-4ec8-925a-bb65fdf41695


# ----------------------------
jira_user = os.environ["JIRA_USER"]
jira_api_key = os.environ["JIRA_API_KEY"]
JIRA_BASE_URL = "https://projectify.atlassian.net/rest/api/3/search/jql"       # e.g. "https://yourcompany.atlassian.net/rest/api/2"
PROJECT = 'KAN'           # e.g. "PROJ"


# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

def fetch_jira_tickets():

  url = "https://projectify.atlassian.net/rest/api/3/search/jql"

  auth = HTTPBasicAuth(jira_user, jira_api_key)

  headers = {
    "Accept": "application/json"
  }

  query = {
    'jql': 'project = KAN ORDER BY created DESC',
    'maxResults': '50',
    'fields': ['summary','description', 'epic link']
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query,
    auth=auth
  )

  data = response.json()

  tickets = []

  for issue in data.get("issues", []):
      key = issue["key"]
      summary = issue["fields"].get("summary", "")

      # Extract description text from ADF
      description = ""
      desc_field = issue["fields"].get("description")

      if desc_field and "content" in desc_field:
          for block in desc_field["content"]:
              if "content" in block:
                  for item in block["content"]:
                      if item["type"] == "text":
                          description += item["text"]

      ticket_url = f"https://projectify.atlassian.net/browse/{key}"

      tickets.append((summary,description,ticket_url))

  return (tickets)

def create_jira_issue(summary, description):
    url = "https://projectify.atlassian.net/rest/api/3/issue"

    auth = HTTPBasicAuth(jira_user, jira_api_key)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {"key": "KAN"},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": description}
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Task"}
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)

    if response.status_code != 201:
        raise Exception(f"Jira creation failed: {response.text}")

    return response.json()["key"]