import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from sage_scraper import * 
from llm_logic import * 
from Jira_issues import * 


app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
)
message_store = {}

@app.event("reaction_added")
def handle_reaction_added(event, client):
    reaction = event.get("reaction")
    channel_id = event["item"]["channel"]
    ts = event["item"]["ts"]

    # I Fetch the original message if not already stored
    if ts not in message_store:
        text_original_message = client.conversations_history(
            channel=channel_id,
            latest=ts,
            inclusive=True,
            limit=1
        )['messages'][0]['text']
        message_store[ts] = text_original_message
    else:
        text_original_message = message_store[ts]

    # Step 1: User reacts with :search-doc emoji: this calls the scraper in sage_scraper.py, then feeds the scrapes articles to an LLM that picks the most relevant.
    if reaction == "search-doc":
        parsed_result_list = parse_documentation(text_original_message)
        search_result = pick_most_relevant_result(text_original_message, parsed_result_list)

        client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=(
                f"Let me have a look in the doc. I found this:\n{search_result}\n\n"
                "If this is not relevant, react with :jira-search: to see the related JIRA tickets, or :jira-new: to create a new issue. "
            )
        )

    # Step 2: User reacts with :jira-search:, the LLM searchs for the most relevant jira issue related to this question
    elif reaction == "jira-search":
        list_jira_tickets = fetch_jira_tickets()
        selected_jira = pick_most_relevant_result(text_original_message, list_jira_tickets)

        client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=f"I found this related Jira ticket for your issue:\n{selected_jira}. If this is not relevant, react with :jira-new: to create a new issue. "
        )
    
# Step 2: User reacts with :jira-new:, the LLM creates a JIRA issue with enriched summary and description.
    elif reaction == "jira-new":

        structured = generate_structured_issue(text_original_message)

        summary = structured["summary"]
        description = structured["description"]

        issue_key = create_jira_issue(summary, description)
        issue_url = f"https://projectify.atlassian.net/browse/{issue_key}"

        client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=f"🎟️ Jira issue created successfully: <{issue_url}|View Jira Issue>"
        )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()