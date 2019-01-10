#!/usr/bin/env python

import argparse
import json
import requests
import time

from urllib3.exceptions import InsecureRequestWarning


def change_light_hue(api_url, light_number, new_hue):
    body = {"hue": new_hue}
    requests.put('{}/lights/{}/state'.format(api_url, light_number), data=json.dumps(body), verify=False)


def get_lights_by_name(name):
    response = requests.put('{}/lights'.format(api_url), verify=False)
    return [light for light in response.json().values() if name.lower() in light['name'].lower()]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Play around with hue lights")
    parser.add_argument("action", help="Perform this action", choices=["colour-cycle"])
    parser.add_argument("--name", help="Filter by lights matching this name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    # TODO: Handle config.json being missing
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    # TODO: Create new username if required and store in config
    # TODO: If IP is missing or wrong, discover and save to config
    api_url = 'https://{}/api/{}'.format(config['hue_ip'], config['hue_username'])
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    lights = get_lights_by_name("kitchen")
    if args.action == "colour-cycle":
        while True:
            for hue in range(0, 65280, 1000):
                for light in lights:
                    change_light_hue(api_url=api_url, light_number=light, new_hue=hue)
                time.sleep(1)
