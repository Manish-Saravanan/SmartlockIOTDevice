import datetime
import datetime
import logging
import os
import random
import ssl
import time

import jwt
import paho.mqtt.client as mqtt

def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
    Args:
     project_id: The cloud project ID this device belongs to
     private_key_file: A path to a file containing either an RSA256 or
             ES256 private key.
     algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
    Returns:
        A JWT generated from the given project_id and private key, which
        expires in 20 minutes. After 20 minutes, your client will be
        disconnected, and a new JWT will have to be generated.
    Raises:
        ValueError: If the private_key_file does not contain a known key.
    """

    token = {
        # The time that the token was issued at
        "iat": datetime.datetime.utcnow(),
        # The time the token expires.
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
        # The audience field should always be set to the GCP project id.
        "aud": project_id,
    }

    # Read the private key file.
    with open(private_key_file, "r") as f:
        private_key = f.read()

    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )

    return jwt.encode(token, private_key, algorithm=algorithm)

def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return "{}: {}".format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print("on_connect", mqtt.connack_string(rc))

    # After a successful connect, reset backoff time and stop backing off.
    global should_backoff
    global minimum_backoff_time
    should_backoff = False
    minimum_backoff_time = 1


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print("on_disconnect", error_str(rc))

    # Since a disconnect occurred, the next loop iteration will wait with
    # exponential backoff.
    global should_backoff
    should_backoff = True


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print("on_publish")


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode("utf-8"))
    print(
        "Received message '{}' on topic '{}' with Qos {}".format(
            payload, message.topic, str(message.qos)
        )
    )


def get_client(
    project_id,
    cloud_region,
    registry_id,
    device_id,
    private_key_file,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client_id = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    print("Device client_id is '{}'".format(client_id))

    client = mqtt.Client(client_id=client_id)

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username="unused", password=create_jwt(project_id, private_key_file, algorithm)
    )

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    mqtt_topic = "/topics/LockRequest"

    client.subscribe(mqtt_topic, qos=1)

    return client

global minimum_backoff_time
global MAXIMUM_BACKOFF_TIME
should_backoff = False

mqtt_topic = "/topics/LockRequest" 

jwt_iat = datetime.datetime.utcnow()
jwt_exp_mins = 120
client = get_client(
    "vocal-gist-315804",
    "us-central1",
    "registry-2",
    "lock123",
    "rsa_private.pem",
    "RS256",
    "roots.pem",
    "mqtt.googleapis.com",
    8883
)

client.loop()

while True:
    # Wait if backoff is required.
    if should_backoff:
        # Otherwise, wait and connect again.
        delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
        print("Waiting for {} before reconnecting.".format(delay))
        time.sleep(delay)
        minimum_backoff_time *= 2
        client.connect("mqtt.googleapis.com", 8333)

    payload = "Hello world"
    print("Sending message.")
    seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
    if seconds_since_issue > 60 * jwt_exp_mins:
        print("Refreshing token after {}s".format(seconds_since_issue))
        jwt_iat = datetime.datetime.utcnow()
        client.loop()
        client.disconnect()
        client = get_client(
            "vocal-gist-315804",
            "us-central1",
            "registry-2",
            "lock123",
            "rsa_private.pem",
            "RS256",
            "roots.pem",
            "mqtt.googleapis.com",
            8883
        )
    # Publish "payload" to the MQTT topic. qos=1 means at least once
    # delivery. Cloud IoT Core also supports qos=0 for at most once
    # delivery.
    client.publish(mqtt_topic, payload, qos=1)
    print("Message sent.")

    # Send events every second. State should not be updated as often
    for i in range(0, 60):
        time.sleep(1)
        client.loop()

