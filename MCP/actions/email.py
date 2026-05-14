import os
import base64
import asyncio
from email.message import EmailMessage
from typing import AsyncGenerator
from langsmith import traceable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# The official scope required by the Users.messages:send endpoint
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Handles Google OAuth2 authentication and returns the Gmail API service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


@traceable(name="Send Email Tool")
async def send_email(to_address: str, subject: str, body: str) -> AsyncGenerator[str, None]:
    """Sends an email using the official Gmail REST API."""
    
    if not to_address or not subject or not body:
        yield "Error: to_address, subject, and body are all required."
        return

    yield f"Preparing to send email to {to_address}...\n"

    try:
        # We use asyncio.to_thread because the Google API client is synchronous 
        # and we don't want to block your Gradio server loop.
        service = await asyncio.to_thread(get_gmail_service)

        # Construct the email message
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to_address
        message['Subject'] = subject

        # Encode the message in base64url as required by the REST API
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        # Hit the Users.messages:send endpoint
        send_message = await asyncio.to_thread(
            service.users().messages().send(userId="me", body=create_message).execute
        )
        
        yield f"\n✅ Success! Email sent. Message ID: {send_message['id']}"

    except Exception as e:
        yield f"\n❌ [GMAIL API ERROR]: {str(e)}"