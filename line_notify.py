import requests
import json


def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"

    with open("credentials/lineNotify_token.json") as filePointer:
        contents = filePointer.read()
    token = json.loads(contents)["token"]

    headers = {
        'Authorization': 'Bearer ' + token # setting authentication
    }
    data = {
        'message': msg
    }
    r = requests.post(url, headers=headers, data=data)