!Readme!

This is a slack / documentation / jira integration which allows to automatically search the documentation, the jira board for each question asked, and create a new JIRA issue if no useful doc article or jira tiket exists. 

The flow is the following : 

A team member asks a question on a slack channel,
- Behavior 1 triggered by emoji :search-doc: on their message. The documentation (here, SAGE HRIS) is scrapped against their message and an LLM (Claude claude-sonnet-4-20250514) decides and posts via a slack bot the most useful article among the scrapped results.
- Behavior 2 triggered by emoji :jira-search: an LLM (Claude claude-sonnet-4-20250514) decides and posts via a slack bot the most relevant JIRA ticket among the existing issues in the board.
- Behavior 3 triggered by :jira-new" an LLM (Claude claude-sonnet-4-20250514) creates a JIRA ticket with enriched description and summary, and posts via a slack bot the created JIRA issue

Recording of the behavior : https://www.loom.com/share/9d5b3c0a42ea4dac9d8c959452a37091
