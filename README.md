!Readme!
-
This Retrieval-augmented generation project that allows a slack / documentation / jira integration for : 

- Documentation research : triggered by emoji :search-doc: on the slack message. The documentation (here, SAGE HRIS) is scrapped against their message and an LLM (Claude claude-sonnet-4-20250514) selects and posts via a slack bot the most useful article among the scrapped results.
- Jira tickets research, triggered by emoji :jira-search: an LLM (Claude sonnet) decides and posts via a slack bot the most relevant JIRA ticket among the existing issues in the board.
- New Jira tiket creation, triggered by :jira-new" an LLM (Claude sonnet) creates a JIRA ticket with enriched description and summary, and posts via a slack bot the created JIRA issue


Prerequisites :
-
1) a Slack app api key
2) a JIRA api key
3) Claude llm api key 

to run : ```python slack_event_handler.py```


https://github.com/user-attachments/assets/e0ccba1d-558c-4d31-b2ff-fbcd8176b2da

