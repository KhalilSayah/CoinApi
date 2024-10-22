import os
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import re
import json

# Define the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    # Check for credentials.json, which is downloaded from Google Cloud Console
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def list_emails():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    # Dictionary to store extracted API keys
    api_keys_dict = {}

    if not messages:
        print('No messages found.')
    else:
        print('Processing messages for API keys...')
        # Regular expression to match API Key format
        api_key_pattern = r'[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}'

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            snippet = msg['snippet']

            # Search for API key pattern in the email snippet
            match = re.search(api_key_pattern, snippet)

            if match:
                api_key = match.group(0)
                print(f'API Key found: {api_key}')

                # Store the API key in the dictionary with the message ID as the key
                api_keys_dict[message['id']] = api_key
            else:
                print(f'No API Key found in message {message["id"]}')

    # Save the API keys dictionary to a JSON file
    with open('api_keys.json', 'w') as json_file:
        json.dump(api_keys_dict, json_file, indent=4)

    print('API keys saved to api_keys.json')

list_emails()
