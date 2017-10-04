import json
import requests
import os
import time
from dbhelper import DBHelper

db = DBHelper()
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


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
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


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# def echo_all(updates):
#     for update in updates["result"]:
#         try:
#             chat_id = update["message"]["chat"]["id"]
#             text = update["message"]["text"]
#             send_msg(chat_id, text)
#         except Exception as e:
#             print(e)


def handle_updates(updates):
    for update in updates["result"]:
        try:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"]["text"]
            items = db.get_items()
            if text in items:
                db.delete_item(text)
                items = db.get_items()
            else:
                db.add_item(text)
                items = db.get_items()
            message = "\n".join(items)
            send_msg(chat_id, message)
        except KeyError:
            pass


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            # echo_all(updates)
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
