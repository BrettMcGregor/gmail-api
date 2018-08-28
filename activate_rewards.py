from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import datetime

# connect to the gmail API - authorise the current user
scopes = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', scopes)
    creds = tools.run_flow(flow, store)
gmail = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

counter = 1

# get all messages from sender contacts@email.woolworthsrewards.com.au in the previous 24 hours
# results = gmail.users().messages().list(userId='me', labelIds=['INBOX'], q=f'after: {datetime.date.today() - datetime.timedelta(days=1)}from:contacts@email.woolworthsrewards.com.au').execute()

results = gmail.users().messages().list(userId='me', labelIds=['INBOX'], q=f'after: {datetime.date.today() - datetime.timedelta(days=1)}').execute()


# above returns a dict so we want the list of messages using the 'messages' key
msg_list = results['messages']
print(len(msg_list))
# iterate through the list of messages
for msg in msg_list:
    try:
        m_id = msg['id']  # use this variable in next line to fetch for all message ids in list
        message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()
        # body = message['payload']['parts'][1]['body']['data']  # get the body of the message
        body = message['payload']['parts'][1]['body']['data']
        html = base64.urlsafe_b64decode(body).decode('utf-8')  # decode to html
        with open(f'{counter}payload-parts.html', 'w', encoding='utf-8') as file:
            print(html, file=file)

    except KeyError:
        try:
            message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()
            body = message['payload']['body']['data']
            html = base64.urlsafe_b64decode(body).decode('utf-8')  # decode to html
            with open(f'{counter}payload-other.html', 'w', encoding='utf-8') as file:
                        print(html, file=file)
        except KeyError:
            message = gmail.users().messages().get(userId='me', id=m_id, format='full').execute()
            body = message['payload']['parts'][0]['parts'][1]['body']['data']
            html = base64.urlsafe_b64decode(body).decode('utf-8')  # decode to html
            with open(f'{counter}payload-weird.html', 'w', encoding='utf-8') as file:
                        print(html, file=file)
    counter += 1

    # for thing in body:
    #     print(thing)
    # print("\n"*10)
    # break

        
    
    # html = base64.urlsafe_b64decode(body).decode('utf-8')  # decode to html
    # with open(f'message{counter}.json', 'w', encoding='utf-8') as file:
    #         print(body, file=file)
    #         break
    #         counter += 1
    # now we only want the offers with activation required. Find them and output to html file
    # if "ACTIVATE NOW" in html:
    #     with open(f'message{counter}.html', 'a', encoding='utf-8') as file:
    #         print(html, file=file)
    #         counter += 1
