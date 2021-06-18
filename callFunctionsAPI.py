import requests
from time import sleep

try:
    with open("token.txt") as tokenFile:
        token = tokenFile.read()
except:
    sleep(2)
    with open("token.txt") as tokenFile:
        token = tokenFile.read()

response = requests.post(
        "https://us-central1-vocal-gist-315804.cloudfunctions.net/sendNotification",
        headers = {
            "Authorisation": "Bearer " + token
            },
        data = {
            "tokens": ["eSd6eFycQqKmdw6-Kzk11h:APA91bGRaH7VDSLt8Kxiwzfxc7jvihFBAhsUUVPh1QoNdpvEDQpvWXsNg7kK9iY8yqgZ7ZG0egc4aaIJeEIGjtNEIsAvvJ2Xx4I5rgqou_DwefQH15413dx-uNKQ3qsrew8h3Ao3Y9ss"]
            }
        )

print(response.text)
