from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import sys
import json
import pathlib

ROOT_PATH = os.path.dirname(pathlib.Path(__file__).parent.absolute())
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOGID = 4634073707460521498
CLIENT_SECRETS = ROOT_PATH + "/client_secrets.json"
CLIENT_TOKEN = ROOT_PATH + "/token.json"

def getCredentials () -> Credentials:

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CLIENT_TOKEN):
        creds = Credentials.from_authorized_user_file(CLIENT_TOKEN, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CLIENT_TOKEN, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return creds

def getBody(post, data=None) -> dict:
    for key in data:
        post[key] = data[key]
    return post

def getPost (data, service):
    # post id exist both blogger and local
    try:
        return service.posts().get(blogId=BLOGID, postId=data['id']).execute()
    except:
        return service.posts().insert(blogId=BLOGID, isDraft=True).execute()

def run(data=None):
    # Get service
    creds = getCredentials()
    service = build('blogger', 'v3', credentials=creds)

    # Get post refers to data['id']. if it refers to none then creat new one.
    post = getPost(data, service)

    # Update content of the draft post with data.
    JsonPost = json.dumps(getBody(post, data), indent=4, ensure_ascii=False)
    service.posts().update(blogId=BLOGID, postId=post['id'], 
        body=json.loads(JsonPost)).execute()

    # Publish the post.
    service.posts().publish(blogId=BLOGID, postId=post['id']).execute()
    return post['id']    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            sys.stdout.write(run(json.load(f)))
    else:
        sys.stdout.write(run())
