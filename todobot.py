import json
import requests
import os

TOKEN = os.environ['BOT_API_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_msg(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    text = updates["result"][last_update]["message"]
    return (chat_id, text)
