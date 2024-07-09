# Tuya-Web App
Cause I can't be bothered to get the home assistant stuff working and create a tuya developer account.

**It's hacky**, but it works! (and it even delivers a Web GUI if you don't want the hassle with home assistant)

## Requirements
- Tuya or "Smart Life" Account
- Python3
- A Server where this can run
- _some_ understanding of Linux
- A MQTT Server like "mosquitto" (optional for the mqtt.py stuff)

## HowTo

- copy `config.json.example` to `config.json` and configure accordingly
- install requirements (`pip3 install -r requirements.txt`)
- run `tuya.py` with `python3 tuya.py`
- Go to `https://127.0.0.1:5000` or whatever you configured with your own reverse proxy
- Check the IDs and match them via on/off
- Fill the `definitions.txt` (see `definitions.txt.example` on a howto)
- Restart `tuya.py` (Ctrl+C in the command line and just re run)
- Check if the names are printed now
- Run `mqtt.py` with `python3 mqtt.py`
- Try if it works


## Running in the background
- Go to your server where you wanna put this stuff
- Clone this repo
- Create systemd/init.d/whatever files to run it in the background
- ...
- profit!

## HomeAssistant Integration

My HomeAssistant Config for this looks like that:

In `configuration.yaml`:

```

mqtt: !include mqtt.yaml #right before script: !include scripts.yaml

```

Create a `mqtt.yaml` in the same directory and fill like this:

```


- light:
      name: uvled
      state_topic: "tuya/uvled/status"
      command_topic: "tuya/uvled/set"
- switch:
      name: strip1_all
      state_topic: "tuya/strip1_all/status"
      command_topic: "tuya/strip1_all/set"
- switch:
      name: strip1_1
      state_topic: "tuya/strip1_1/status"
      command_topic: "tuya/strip1_1/set"

```

The mqtt will always use `tuya/<devicename>/status` & `tuya/<devicename>/set` as topics!

## Known Limitations

- Only on/off states are supported
- MAYBE only devices that only have on/off states are supported (definitly not tested due to the lack of such device)
- You need to wait 180s before respawning tuya.py (this is due to the API limitations if you don't want a dev account (WHICH I DON'T!))

## FAQ
### Docker
Nope. Create a PR and I'll happily merge it :>
### Do I need a developer account with tuya?
**NO** you don't need a developer account. An "Tuya" / "Smart Life" (App)Account is sufficient!
### Which types can I add?
Currently you can add anything that's just "ON"/"OFF"

I happily accept PR's for anything else, but can't test it due to the lack of devices that have more features.
### I'm a nazi. Can I use this?
**No!** Please don't and please go away!
### Explain the config.json please
Okay, here we go:
#### username
your username for Smart Life / Tuya App (most likely your email address. DOES NOT WORK WITH PHONE NUMBER!)
#### password
your password. Yes. Unencrypted. Unhashed. No I won't send it to "my servers". You can either trust me or check the code :)
#### country_code
It's no country code anymore but now "Datacenter Regions" in our case "EU" but "CN" should also be valid if you have a very old account (or "US" if you're from the other side of the big ocean)
#### web_endpoint
Where the flask application (`tuya.py`) lifes. You can either put https://127.0.0.1:5000 there if it's just on the same server or configure your caddy/nginx/whatever to have a proper domain
#### mqtt_broker
your mqtt server
#### mqtt_port
for the edge case where you don't have 1883 as your port
#### mqtt_username/mqtt_password
If you don't do auth, just use `""` as username. Otherwise put them in (YES cleartext)
### Can you give an example how to run it in the background?
Sure. Thats how I've done it:

```

[Unit]
Description=run tuyawebapp
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/tuyaweb/tuya-web/tuya.py
Restart=always
User=tuyaweb
Group=tuyaweb
WorkingDirectory=/hom/tuyaweb/tuya-web

[Install]
WantedBy=multi-user.target

```

&& 

```

[Unit]
Description=run tuyaweb mqtt middleware
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/tuyaweb/tuya-web/mqtt.py
Restart=always
User=tuyaweb
Group=tuyaweb
WorkingDirectory=/hom/tuyaweb/tuya-web

[Install]
WantedBy=multi-user.target

```

Place these files as "tuyaweb.service" & "tuyamqtt.service" in `/etc/systemd/system` do a `sudo systemctl daemon-reload` & `sudo systemctl enable tuyaweb.service tuyamqtt.service` & `sudo systemctl start tuyaweb.service tuyamqtt.service`

Please be aware that this will only work when you create a user `tuyaweb` and clone the repo in the home of the user

