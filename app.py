import logging
from flask import Flask, session
from flask_ask import Ask, statement
import os
import wunderpy2
import difflib

api = wunderpy2.WunderApi()
access_token = os.environ.get('ACCESS_TOKEN')
client_id = os.environ.get('CLIENT_ID')
client = api.get_client(access_token=access_token, client_id=client_id)


SAVED_REQUESTS = {}

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.intent("AddTask")
def add_task(task, task_list):
    if not task or not task_list:
        return statement("I'm sorry, I did not hear what you wanted to put on the list")

    lists = client.get_lists()
    list_names = [l[u'title'] for l in lists]
    close_matches = difflib.get_close_matches(task_list, list_names)

    if len(close_matches) < 1:
        return statement("I could not understand which list you want me to use")

    intended_list_name = close_matches[0]

    chosen_list = None
    for l in lists:
        if l[u'title'] == intended_list_name:
            chosen_list = l
            break

    if not chosen_list:
        return statement("I could not find the {0!s} list".format(task_list))

    res = client.create_task(chosen_list[u'id'], task)

    if u'id' not in res:
        return statement("I could not add {0!s} to the {1!s} list".format(task, task_list))

    return statement('Done')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
