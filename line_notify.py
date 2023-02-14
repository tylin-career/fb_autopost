import requests
import json
from logger import Logger
import os
logger = Logger(__name__).get_logger()

def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        'Authorization': 'Bearer ' + str(token) # setting authentication
    }
    data = {
        'message': msg
    }
    r = requests.post(url, headers=headers, data=data)
    print(f"status_code: {r.status_code}")


def get_token():
    abs_path = os.path.dirname(os.path.abspath("__file__"))
    cred_path = os.path.join(abs_path, "data\\credentials\\lineNotify_token.json")
    print(cred_path)
    try:
        with open(cred_path) as filePointer:
            contents = filePointer.read()
        token = json.loads(contents)['token']
        logger.info(f"Line token loaded.")
        return token
    except:
        logger.info(
            "Failed to retrieve your line token."
        )