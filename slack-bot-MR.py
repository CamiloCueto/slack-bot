import os
import slack
import json
from time import sleep
from pathlib import Path
from dotenv import load_dotenv

CHANNEL='C03KZ0QBNBV'
MESSAGES_PER_PAGE = 200
MAX_MESSAGES = 1000

# init variables token
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

# traer primera pagina
page = 1
print("Retrieving page {}".format(page))
response = client.conversations_history(
    channel=CHANNEL,
    limit=MESSAGES_PER_PAGE,
)
assert response["ok"]
messages_all = response['messages']

# traer paginas adicionales
while len(messages_all) + MESSAGES_PER_PAGE <= MAX_MESSAGES and response['has_more']:
    page += 1
    print("Retrieving page {}".format(page))
    sleep(1)   # sleep 1seg debido a rate limit
    response = client.conversations_history(
        channel=CHANNEL,
        limit=MESSAGES_PER_PAGE,
        cursor=response['response_metadata']['next_cursor']
    )
    assert response["ok"]
    messages = response['messages']
    messages_all = messages_all + messages

print(
    "Fetched a total of {} messages from channel {}".format(
        len(messages_all),
        CHANNEL
))

# escribe el resultado en json
with open('messages.json', 'w', encoding='utf-8') as f:
  json.dump(
      messages_all, 
      f, 
      sort_keys=True, 
      indent=4, 
      ensure_ascii=False
    )