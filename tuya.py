import json
import time
from flask import Flask, render_template, redirect, url_for, send_from_directory
from tuyapy import TuyaApi

app = Flask(__name__)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

def load_definitions():
    definitions = {}
    with open('definitions.txt', 'r') as definitions_file:
        for line in definitions_file:
            if '=' in line:
                device_id, name = line.strip().split('=')
                definitions[device_id.strip()] = name.strip().strip('"')
    return definitions

definitions = load_definitions()
api = TuyaApi()
last_auth_time = 0

def authenticate():
    global last_auth_time
    if time.time() - last_auth_time > 180:
        api.init(config['username'], config['password'], config['country_code'])
        last_auth_time = time.time()

@app.route('/')
def index():
    authenticate()
    try:
        devices = api.get_all_devices()
    except Exception as e:
        print(f"Fehler beim Abrufen der Geräte: {e}")
        devices = []
    return render_template('index.html', devices=devices, definitions=definitions)

@app.route('/public/<path:filename>')
def public_files(filename):
    return send_from_directory('public', filename)

@app.route('/<device_id>/on')
def turn_on(device_id):
    authenticate()
    device = api.get_device_by_id(device_id)
    if device:
        device.turn_on()
    return redirect(url_for('index'))

@app.route('/<device_id>/off')
def turn_off(device_id):
    authenticate()
    device = api.get_device_by_id(device_id)
    if device:
        device.turn_off()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
