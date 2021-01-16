import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailClient:
    __creds = None
    __client = None

    def __init__(self, credentials_file, scopes):
        self.__credentials_file = credentials_file
        self.__scopes = scopes
        self.__client = self.__authenticate_gmail()

    def search_emails_from(self, sender):
        result = self.__client.users().messages().list(userId="me",q=sender).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])

        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.__client.users().messages().list(userId="me", q=sender, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])

        return messages

    def bulk_delete_emails(self, emails):
        return self.__client.users().messages().batchDelete(
            userId="me",
            body={
                'ids': [ email['id'] for email in emails ]
            }
        ).execute()

    def __authenticate_gmail(self):
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.__creds = pickle.load(token)
        
        # if there are no (valid) credentials availablle, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__credentials_file, self.__scopes)
                self.__creds = flow.run_local_server(port=0)

            # save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.__creds, token)

        return build('gmail', 'v1', credentials=self.__creds)
       
        