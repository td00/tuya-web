import json
import paho.mqtt.client as mqtt
import requests

with open('config.json') as config_file:
    config = json.load(config_file)
device_map = {}
with open('definitions.txt') as definitions_file:
    for line in definitions_file:
        device_id, device_name = line.strip().split('=')
        device_map[device_name.strip('"')] = device_id
web_endpoint = config['web_endpoint']
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for device_name in device_map.keys():
        client.subscribe(f"tuya/{device_name}/set")
        print(f"Subscribed to tuya/{device_name}/set")

def on_message(client, userdata, msg):
    device_name = msg.topic.split('/')[1]
    command = msg.payload.decode().strip().upper()
    device_id = device_map.get(device_name)

    if command in ['ON', 'OFF'] and device_id:
        action = command.lower()
        url = f"{web_endpoint}/{device_id}/{action}"
        response = requests.get(url)

        if response.status_code == 200:
            client.publish(f"tuya/{device_name}/status", command)
            print(f"Device {device_name} ({device_id}) turned {command}")
        else:
            print(f"Failed to turn {command} device {device_name} ({device_id}): {response.status_code}")

client = mqtt.Client()
client.username_pw_set(config['mqtt_username'], config['mqtt_password'])
client.on_connect = on_connect
client.on_message = on_message

client.connect(config['mqtt_broker'], config['mqtt_port'], 60)
client.loop_forever()

