import logging
from flask import Flask
from flask_ask import Ask, statement, question
import os
import wunderpy2
import difflib

api = wunderpy2.WunderApi()
access_token = os.environ.get('ACCESS_TOKEN')
client_id = os.environ.get('CLIENT_ID')
client = api.get_client(access_token=access_token, client_id=client_id)


SAVED_REQUESTS = {}

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

GROCERY_LIST_NAME = "Grocery"
GROCERY_LIST_ID = os.environ.get("GROCERY_LIST_ID")


@ask.default_intent
@ask.intent("AddTask")
def add_task(task):

    app.logger.info("Got {} to put on {}".format(task, GROCERY_LIST_NAME))

    if not task:
        return question("I'm sorry, could you repeat that please?")

    res = client.create_task(GROCERY_LIST_ID, task)
    print(res)
    if u'id' not in res:
        return statement("I could not add {0!s} to the {1!s} list".format(task, GROCERY_LIST_NAME))

    # card_text = "{} added to {}".format(task, task_list)
    return question("Anything else?")


@ask.default_intent
@ask.intent("NoIntent")
def no():
    return statement("OK, I have updated your {} list.".format(GROCERY_LIST_NAME))


def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
