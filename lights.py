#!/usr/bin/env python

import argparse
import json
import requests
import time

from urllib3.exceptions import InsecureRequestWarning


# TODO: Make class for all api calls

def change_light_hue(api_url, light_number, new_hue):
    body = {"hue": new_hue}
    requests.put('{}/lights/{}/state'.format(api_url, light_number), data=json.dumps(body), verify=False)


def get_light_numbers_by_name(api_url, name):
    print("Getting lights")
    light_json = requests.get('{}/lights'.format(api_url), verify=False).json()
    return [key for key in light_json.keys() if name.lower() in light_json[key]['name'].lower()]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Play around with hue lights")
    parser.add_argument("action", help="Perform this action", choices=["colour-cycle"])
    parser.add_argument("--name", help="Filter by lights matching this name", dest='name')
    return parser.parse_args()


def turn_lights_on(api_url, light_numbers):
    for light_number in light_numbers:
        body = {"on": True}
        requests.put('{}/lights/{}/state'.format(api_url, light_number), data=json.dumps(body), verify=False)


if __name__ == "__main__":
    args = parse_arguments()
    # TODO: Handle config.json being missing
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    print(config)
    # TODO: Create new username if required and store in config
    # TODO: If IP is missing or wrong, discover and save to config
    api_url = 'https://{}/api/{}'.format(config['hue_ip'], config['hue_username'])
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    lights = get_light_numbers_by_name(api_url=api_url, name=args.name)
    print("Lights: {}".format(lights))
    turn_lights_on(api_url=api_url, light_numbers=lights)
    if args.action == "colour-cycle":
        while True:
            for hue in range(0, 65280, 1000):
                for light in lights:
                    change_light_hue(api_url=api_url, light_number=light, new_hue=hue)
                time.sleep(1)
