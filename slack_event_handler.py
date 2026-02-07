import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from sage_scraper import * 
from llm_picking_articles import * 

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
)

@app.event("reaction_added")
def handle_reaction_added(event, client):
    reaction = event.get("reaction")
    channel_id = event["item"]["channel"]
    ts = event["item"]["ts"]
    #event["item"]["ts"] fetches the event that received the reaction, not the event OF the reaction

    if reaction == "raccoon":
        global text_original_message
        text_original_message = client.conversations_history(channel=channel_id,latest =event["item"]["ts"],inclusive=True,)['messages'][0]['text']
        parsed_result_list = parse_documentation(text_original_message)
        search_result =  pick_most_relevant_result(text_original_message,parsed_result_list)
        client.chat_postMessage(
            channel= event["item"]["channel"],
            text=f"let me have a look in the doc. I found this : {search_result}"
        )
        
    #client.conversations_history is a python sdk method
   
if __name__ == "__main__":
   handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
   handler.start()

