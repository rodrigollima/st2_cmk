import argparse
import requests
import yaml
import json
import sys

def get_payload(args):
    try:
        payload = {}
        payload['event_id'] = args[0]
        payload['service'] = args[1]
        payload['state'] = args[2]
        payload['state_id'] = args[3]
        payload['state_type'] = args[4]
        payload['attempt'] = args[5]
        payload['host'] = args[6]
        payload['output'] = args[7]

        return payload
    except IndexError:
        print('Number of Arguments given to the handler are incorrect')
        sys.exit(1)

def main(config, payload):
    with open(config) as f:
        config = yaml.safe_load(f)
        API_KEY = config.get('API_KEY', None)
        API_HOST = config.get('API_HOST', None)
        SSL_VERIFY = config.get('SSL_VERIFY', False)
        ST2_TRIGGER = config.get('ST2_TRIGGER', False)
        
        headers = {
            'St2-Api-Key' : API_KEY,
            'Content-Type': 'application/json'
        }

        data = {
            "trigger" : ST2_TRIGGER,
            "payload" : payload
        }

        try:
            r = requests.post(API_HOST, headers=headers, data=json.dumps(data), verify=SSL_VERIFY)
        except Exception as r:
            print(r)
            sys.exit(1)

if __name__ == '__main__':
    description = '\nStackStorm check_mk event handler. Please provide args '\
        'in following order after the config_path:\n\n event_id, service, '\
        'state, state_id, state_type, attempt, host, output\n'

    parser = argparse.ArgumentParser(description)
    parser.add_argument('config_path',help='Exchange to listen on')
    parser.add_argument('--verbose', '-v', required=False, action='store_true',help='Verbose mode.')

    args, nargs = parser.parse_known_args()
    payload = get_payload(nargs)

    main(config=args.config_path, payload=payload)
