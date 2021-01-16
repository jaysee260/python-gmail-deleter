# Prerequisites
You'll need Python and pip installed. Whatever the latest versions are at the time will do.

# Usage

1. Clone this repository.
1. Populate array in `senders.json` with 1 or more email addresses.
1. Go to [this tutorial](https://developers.google.com/gmail/api/quickstart/python) by Google and follow the instructions in Step 1 to enable use of the Gmail API in your account (needless to say, you'll need a Google account). After you're done with Step 1, you will have a `credentials.json` file.
1. Save `credentials.json` at the root of this project.
1. Restore dependencies by running `pip install --upgrade -r requirements.txt`.
1. Run `python delete_emails_by_sender.py`.