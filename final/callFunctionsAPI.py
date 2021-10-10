import requests
from time import sleep
import jwt
import json
import base64


try:
    with open("token.txt") as tokenFile:
        token = tokenFile.read()
except:
    sleep(2)
    with open("token.txt") as tokenFile:
        token = tokenFile.read()

try:
    with open("deviceTokens.txt") as deviceTokensFile:
        deviceTokens = json.loads(deviceTokensFile.read())["tokens"]
except:
    sleep(2)
    with open("deviceTokens.txt") as deviceTokensFile:
        deviceTokens = json.loads(deviceTokensFile.read())["tokens"]

with open("image.jpg", "rb") as image_file:
    imageData = base64.b64encode(image_file.read())

response = requests.post(
        "http://us-central1-vocal-gist-315804.cloudfunctions.net/sendNotification",
        headers = {
            "authorization": "Bearer " + token
            },
        data = {
            "tokens": deviceTokens,
            "imageData": imageData
            }
        )
