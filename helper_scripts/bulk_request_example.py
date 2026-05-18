#!/usr/bin/env python
import os
from datetime import datetime, timedelta
import json
import requests
from typing import List, Dict, Any


GATEKEEPER_BASE_URL = 'http://localhost:8001'
LOGIN_URL = url = f"{GATEKEEPER_BASE_URL}/api/login/"
SERVICE_BASE_URL = f'{GATEKEEPER_BASE_URL}/api/proxy/farmcalendar'
API_ENDPOINT = '/api/v1/bulk/animal-lactating-activities'
API_URL = f'{SERVICE_BASE_URL}{API_ENDPOINT}'
API_URL = f'http://localhost:8002{API_ENDPOINT}'


def get_auth_token(username, passsword):

    # data = {
    #     "username": username,
    #     "password": passsword
    # }
    # response = requests.post(url, data=data)

    # if response.status_code == 200:
    #     # Extract tokens from the JSON response
    #     tokens = response.json()
    #     token = tokens.get("access")


    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_calendar.settings')
    import jwt
    from django.conf import settings
    payload = {
        'user_id': '1',
        'exp': datetime.utcnow() + timedelta(days=1),
        'token_type': 'access',
    }

    token = jwt.encode(payload, settings.JWT_SIGNING_KEY, algorithm=settings.JWT_ALG)

    return token


def send_bulk_request(bulk_data: List[Dict[str, Any]], auth_token):
    """Send bulk request to API."""
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response = requests.post(API_URL, json=bulk_data, headers=headers)
    return response


if __name__ == "__main__":

    with open('farm_calendar_animals_bulk.json', 'r') as f:
        bulk_data = json.load(f)

    # Generate token
    auth_token = get_auth_token('admin', 'admin')
    # Convert to bulk format

    # Send request
    response = send_bulk_request(bulk_data, auth_token)

    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.text}")
