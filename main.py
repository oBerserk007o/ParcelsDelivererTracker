import requests
import json

sadge = ""
change_settings = False
settings_to_change = []
trackingUrl = 'https://parcelsapp.com/api/v3/shipments/tracking'
try:
    with open("info.json", "r") as f:
        info = json.load(f)
except:
    info = {}


try:
    change_settings = 'Y' in input("Do you want to change the settings from last time? [Y/n] > ")
    if not change_settings:
        with open("info.json", "r") as f:
            info = json.load(f)
    else:
        settings_to_change = input("Which do you want to change? \n1: api key\n2: tracking id\n3: country\n4: banned words "
                                   "\n(put the numbers joined together) > ").strip(",. -_abcdefghijklmnopqrstuvwxyz")
except FileNotFoundError:
    print("File 'info.json' not found (just change the settings from start)")
    exit()


if change_settings:
    if "1" in settings_to_change:
        info["api_key"] = input("New api key (https://parcelsapp.com/dashboard/#/admin/dashboard) > ")
    if "2" in settings_to_change:
        info["tracking_id"] = input("New tracking ID > ")
    if "3" in settings_to_change:
        info["country"] = input("New country (capitalized) > ")
    if "4" in settings_to_change:
        info["banned"] = input("New banned delivery services "
                                                     "(separate only with comma (',' not ', ')) > ").split(",")


with open("info.json", "w") as f:
    json.dump(info, f, indent=2)


shipments = [
    {'trackingId': info["tracking_id"], 'language': 'en', 'country': info["country"]}
]

response = requests.post(trackingUrl, json={'apiKey': info["api_key"], 'shipments': shipments}).json()

if "error" not in response.keys():
    for i in range(len(response["shipments"][0]["services"])):
        slug = response["shipments"][0]["services"][i]
        for banned in info["banned"]:
            if banned in slug["name"]:
                sadge = banned

    if sadge != "":
        print(f"I'm sorry for your loss, but it is delivered with {sadge}")
    else:
        print("Package is not delivered by blacklisted company")
else:
    if "description" in response.keys():
        message = f"Something went wrong: '{response['error']}: {response['description']}', please retry with correct settings"
    else:
        message = f"Something went wrong: '{response['error']}', please retry with correct settings"
    print(message)

with open("response.json", "w") as file:
    json.dump(response, file, indent=2)

