from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import datetime

"""
Requirements:
Need to have the google api python client library installed.
Connect to the gmail API - authorise the current user.
Scopes are strings which identify resources that the app needs to access.
"""

scopes = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', scopes)
    creds = tools.run_flow(flow, store)
gmail = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

# here we get a listing of messages meeting the argument criteria (returns json dictionary)
# The combination of 'labelIds' and 'q' (query) enables selection of the email(s) required
results = gmail.users().messages().list(userId='me', labelIds=['INBOX'], q=f'after: {datetime.date.today() - datetime.timedelta(days=1)}').execute()

# above returns a dict so we want the list of messages using the 'messages' key
msg_list = results['messages']
print(f"{len(msg_list)} email messages being processed...")  # see how many messages returned by results query

# iterate through the list of messages
# there are different types of message format so accessing the desired element of the dictionary varies. Three cases so far. Use try and except for each case.
counter = 1
for msg in msg_list:
    m_id = msg['id']  # use this variable in next line to fetch for all message ids in list
    try:        
        message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()  # get a message from the list
        body = message['payload']['parts'][1]['body']['data']  # get the body of the message. This is where there is variation (compare other try blocks)
        html = base64.urlsafe_b64decode(body).decode('utf-8')  # decode to html
        with open(f'{counter}payload-type1.html', 'w', encoding='utf-8') as file:  # save the decoded body to a file
            print(html, file=file)

    except KeyError:
        try:
            message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()
            body = message['payload']['body']['data']
            html = base64.urlsafe_b64decode(body).decode('utf-8')
            with open(f'{counter}payload-type2.html', 'w', encoding='utf-8') as file:
                print(html, file=file)
        except KeyError:
            message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()
            body = message['payload']['parts'][0]['parts'][1]['body']['data']
            html = base64.urlsafe_b64decode(body).decode('utf-8')
            with open(f'{counter}payload-type3.html', 'w', encoding='utf-8') as file:
                print(html, file=file)
    except IndexError:
        # try:
            message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()
            body = message['payload']['parts'][0]['body']['data']
            html = base64.urlsafe_b64decode(body).decode('utf-8')
            with open(f'{counter}payload-type4.html', 'w', encoding='utf-8') as file:
                print(html, file=file)
    counter += 1
