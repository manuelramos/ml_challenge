import sys
from getpass import getpass
import imaplib
import datetime
import email 
import email.header
from database import DataBase

from sqlalchemy import String, BigInteger

EMAIL_ACCOUNT = 'manuelramos175@gmail.com'
IMAP_SERVER = 'imap.gmail.com'

# TODO: move this info to env variables
DB_USERNAME = 'user'
DB_PASSWORD = 'user'
DB_NAME = 'gemails'
TABLE_SPEC = [
    ('id', BigInteger),
    ('from', String(255)),
    ('subject', String(255)),
    ('date', String(255))
]


def get_emails_data(imap_server, username, password, search_criteria):
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    try:
        M.login(username, password)
    except imaplib.IMAP4.error:
        print('Login failed.')
        sys.exit(1)
    M.select("inbox")
    status, search_data = M.search(None, search_criteria)

    if status != 'OK':
        print("No messages found!")
        return

    result = []
    for email_id in search_data[0].split():
        typ, email_data = M.fetch(email_id, '(RFC822)')
        if typ != 'OK':
            print("ERROR on fetch message", email_id)
            return
        decoded_mge = email_data[0][1].decode('utf-8')
        msg = email.message_from_string(decoded_mge)
        msg_data = dict()
        msg_data['id'] = int(email_id)
        msg_data['subject'] = msg['Subject']
        msg_data['from'] = msg['From']
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime \
                .fromtimestamp(email.utils.mktime_tz(date_tuple))
            msg_data['date'] = local_date.strftime("%a, %d %b %Y %H:%M:%S")
        result.append(msg_data)

    M.logout()
    return result


SEARCH_CRITERIA = '(OR SUBJECT Devops BODY Devops)'
data = get_emails_data(IMAP_SERVER,
                       EMAIL_ACCOUNT,
                       getpass(),  # Input for gmail email account pwd
                       SEARCH_CRITERIA)
db = DataBase('mysql://{}:{}@127.0.0.1:3306/{}'
              .format(DB_USERNAME, DB_PASSWORD, DB_NAME))
db.create_table('emails_data', TABLE_SPEC)
db.insert_data('emails_data', data, TABLE_SPEC)
