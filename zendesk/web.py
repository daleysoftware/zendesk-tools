import json
import requests

def read_json_from_url(url, auth=None):
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers, auth=auth)
    return json.loads(response.text)