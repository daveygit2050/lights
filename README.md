# lights

An app for mucking around with Phillips Hue lights.

## Setup

1. Install requirements with `pipenv install`
1. Activate virtual environment with `pipenv shell`
1. Create a `config.json` with your Hue Bridge IP and username (see below)
1. Run `./lights.py --help` for usage instructions

## Setting up your config.json

Currently this is done manually, but may be automated in future.

First, you need to find out your Hue Bridge IP. This can be found within the Hue mobile app under Settings > Hue Bridges.

Next, you need to generate an API username. To do so, follow [these instructions](https://developers.meethue.com/develop/get-started-2/).

Once you have both create a file called config.json as follows...

```json
{
        "hue_ip": "{hue-bridge-ip-address}",
        "hue_username": "{api-username}"
}
```

