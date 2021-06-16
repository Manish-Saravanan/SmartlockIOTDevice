from firebase_admin import messaging

# The topic name can be optionally prefixed with "/topics/".
topic = 'highScores'

# See documentation on defining a message payload.
message = messaging.Message(
    data={
        'score': '850',
        'time': '2:45',
    },
    topic=topic,
)

# Send a message to the devices subscribed to the provided topic.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)
