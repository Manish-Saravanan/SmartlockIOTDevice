import time

from google.cloud import pubsub_v1

# TODO(developer)

project_id = "vocal-gist-315804"
topic_id = "LockRequest"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

futures = dict()

def get_callback(f, data):
    def callback(f):
        try:
            print(f.result())
            futures.pop(data)
        except:  # noqa
            print("Please handle {} for {}.".format(f.exception(), data))

    return callback

import base64
from PIL import Image
from io import BytesIO

with open("image.jpg", "rb") as image_file:
    data = base64.b64encode(image_file.read())

futures.update({data: None})
# When you publish a message, the client returns a future.
future = publisher.publish(topic_path, data)
futures[data] = future
# Publish failures shall be handled in the callback function.
future.add_done_callback(get_callback(future, data))

# Wait for all the publish futures to resolve before exiting.
while futures:
    time.sleep(5)

print(f"Published messages with error handler to {topic_path}.")
