import Lib as mqtt

client = mqtt.get_client("vocal-gist-315804", "us-central1", "registry-2", "lock123", "rsa_private.pem", "RS256", "roots.pem", "mqtt.googleapis.com", 8883)

mqtt.attach_device(client, "lock123", "")

print("Attached to bridge.")

mqtt.listen_for_messages("", "vocal-gist-315804", "us-central1", "registry-2", "lock123", 5, "rsa_private.pem", "RS256", "roots.pem", "mqtt.googleapis.com", 8883, 120, 120)

