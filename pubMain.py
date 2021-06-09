import MQTTPubLib as mqtt

client = mqtt.get_client("vocal-gist", "us-central1", "registry-2", "lock123", "rsa_private.pem", "RS256", "roots.pem", "mqtt.googleapis.com", 8883)


client = mqtt.
