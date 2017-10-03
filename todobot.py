import json
import requests
import os
import time

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


def send_msg(chat_id, text):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_chat = (None, None)
    while True:
        chat_id, text, = get_last_msg(get_updates())
        if (chat_id, text) != last_chat:
            send_msg(chat_id, text)
            last_chat = (chat_id, text)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
