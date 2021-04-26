from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import sys
import json
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOGID = 4634073707460521498

def getCredentials () -> Credentials:
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def getBody(post, data=None) -> dict:
    for key in data:
        post[key] = data[key]
    return post

def run(data=None):
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
            print(json.dumps(data, indent=4))
            quit()

    # Get service
    creds = getCredentials()
    service = build('blogger', 'v3', credentials=creds)

    # Create a new draft post.
    newpost = service.posts().insert(blogId=BLOGID, isDraft=True).execute()

    # Update content of the new draft post with data.
    JsonPost = json.dumps(getBody(newpost, data), indent=4, ensure_ascii=False)
    service.posts().update(blogId=BLOGID, postId=newpost['id'], 
        body=json.loads(JsonPost)).execute()

    # Publish the new post.
    service.posts().publish(blogId=BLOGID, postId=newpost['id']).execute()

if __name__ == '__main__':
    run()
