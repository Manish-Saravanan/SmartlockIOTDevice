import argparse
import io
import os
import sys
import time

from google.api_core.exceptions import AlreadyExists
from google.cloud import iot_v1
from google.cloud import pubsub
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as gp_field_mask
from googleapiclient import discovery
from googleapiclient.errors import HttpError


project_id = 'vocal-gist-315804'
cloud_region = 'us-central1'
pubsub_topic = 'door-unlocked'
registry_id = 'registry-2'
device_id = 'lock123'

def createRegistry():
    client = iot_v1.DeviceManagerClient()
    parent = f"projects/{project_id}/locations/{cloud_region}"

    if not pubsub_topic.startswith("projects/"):
        pubsub_topic = "projects/{}/topics/{}".format(project_id, pubsub_topic)

    body = {
            "event_notification_configs": [{"pubsub_topic_name": pubsub_topic}],
            "id": registry_id,
            }

    try:
        response = client.create_device_registry(
                request={"parent": parent, "device_registry": body}
                )
        print("Created registry")
        return response
    except HttpError:
        print("Error, registry not created")
        raise
    except AlreadyExists:
        print("Error, registry already exists")
        raise

def addDevice():
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open("rsa_cert.pem") as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [
            {
                "public_key": {
                    "format": iot_v1.PublicKeyFormat.RSA_X509_PEM,
                    "key": certificate,
                }
            }
        ],
    }

    return client.create_device(request={"parent": parent, "device": device_template})

addDevice()
