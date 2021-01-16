import json
from gmail_client import GmailClient

def read_senders_from(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        return data["senders"]

file_name = "senders.json"
senders = read_senders_from(file_name)

if len(senders) == 0:
    print(f'No senders have been specified in {file_name}.')
    print('Exitting script.')
    quit()

deleted_emails_count = 0
gmail_client = GmailClient(
    credentials_file='credentials.json',
    scopes=['https://mail.google.com/']
)

for sender in senders:
    emails = gmail_client.search_emails_from(sender)
    print(f'Found {len(emails)} emails from {sender}.')
    # TODO: If more than 1,000 emails found for a given sender, split delete into batches
    if len(emails) > 0:
        if len(emails) <= 1000:
            print('Deleting them...\n')
            gmail_client.bulk_delete_emails(emails)
            deleted_emails_count += len(emails)
        else:
            print(f'More than 1,000 emails found from {sender}.')
            print('This exceeds Google\'s max of 1000 ids per request.')
            print(f'Skipping deletion of emails from {sender}.')
            print('Implement the ability to split deletes into batches and retry.\n')
    else:
        print('Skipping.\n')

print(f'Deleted a total of {deleted_emails_count} emails')