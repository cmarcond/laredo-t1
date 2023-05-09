import base64
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'google_credentials.json'

def get_credentials():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    return creds

def send_email(to, subject, body):
    try:
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)

        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(F"Message sent to {to} with Message Id: {send_message['id']}")
    except HttpError as error:
        print(F"An error occurred: {error}")
        send_message = None
    return send_message

send_email(RECEIVER_EMAIL, "GitLab Pipeline Job Completed", "The GitLab pipeline job is done.")
