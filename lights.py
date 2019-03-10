#!/usr/bin/env python

import argparse
import json
import random
import requests
import time

from urllib3.exceptions import InsecureRequestWarning


# TODO: Make class for all api calls

def change_lights_hue(api_url, light_numbers, new_hue):
    body = {"hue": new_hue}
    for light_number in light_numbers:
        requests.put('{}/lights/{}/state'.format(api_url, light_number), data=json.dumps(body), verify=False)


def get_light_numbers_by_name(api_url, name):
    print("Getting lights")
    light_json = requests.get('{}/lights'.format(api_url), verify=False).json()
    return [key for key in light_json.keys() if name.lower() in light_json[key]['name'].lower()]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Play around with hue lights")
    parser.add_argument("action", help="Perform this action", choices=["colour-cycle", "jumper", "race", "random"])
    parser.add_argument("--name", help="Filter by lights matching this name", dest='name')
    parser.add_argument("--sleep", help="Time in seconds to wait between changes", dest='sleep', type=float, default=1)
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
    bridge_api_url = 'https://{}/api/{}'.format(config['hue_ip'], config['hue_username'])
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    lights = get_light_numbers_by_name(api_url=bridge_api_url, name=args.name)
    print("Lights: {}".format(lights))
    turn_lights_on(api_url=bridge_api_url, light_numbers=lights)
    if args.action == "colour-cycle":
        while True:
            for hue in range(0, 65280, 1000):
                change_lights_hue(api_url=bridge_api_url, light_numbers=lights, new_hue=hue)
                time.sleep(args.sleep)
    elif args.action == "jumper":
        while True:
            hot_light = random.choice(lights)
            change_lights_hue(
                api_url=bridge_api_url,
                light_numbers=[hot_light],
                new_hue=0
            )
            change_lights_hue(
                api_url=bridge_api_url,
                light_numbers=[light for light in lights if light != hot_light],
                new_hue=39000)
            time.sleep(args.sleep)
    elif args.action == "random":
        while True:
            for light in lights:
                change_lights_hue(
                    api_url=bridge_api_url,
                    light_numbers=[light],
                    new_hue=random.choice(range(0, 65280))
                )
            time.sleep(1)
    elif args.action == "race":
        while True:
            for light in lights:
                change_lights_hue(
                    api_url=bridge_api_url,
                    light_numbers=[light],
                    new_hue=0
                )
                change_lights_hue(
                    api_url=bridge_api_url,
                    light_numbers=[other for other in lights if other != light],
                    new_hue=39000
                )
                time.sleep(args.sleep)


