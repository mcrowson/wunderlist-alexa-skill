import logging
from flask import Flask
from flask_ask import Ask, statement
import os
import wunderpy2

api = wunderpy2.WunderApi()
access_token = os.environ.get('ACCESS_TOKEN')
client_id = os.environ.get('CLIENT_ID')
client = api.get_client(access_token=access_token, client_id=client_id)


SAVED_REQUESTS = {}

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.intent("AddTask")
def add_task(Task):
    if not Task:
        return statement("I'm sorry, I did not hear what you wanted to put on the list")

    task_list = u'Groceries'
    lists = client.get_lists()

    chosen_list = None
    for l in lists:
        if l[u'title'] == task_list:
            chosen_list = l
            break

    if not chosen_list:
        return statement("I could not find the grocery list")

    res = client.create_task(chosen_list[u'id'], Task)

    if u'id' not in res:
        return statement("I could not add {} to the grocery list")

    return statement('Done')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
