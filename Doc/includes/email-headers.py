# Import the email modules we'll need
#from email.parser import BytesParser
from email.parser import Parser
from email.policy import default

# If the e-mail headers are in a file, uncomment these two lines:
# with open(messagefile, 'rb') as fp:
#     headers = BytesParser(policy=default).parse(fp)

#  Or for parsing headers in a string (this is an uncommon operation), use:
headers = Parser(policy=default).parsestr(
        'From: Foo Bar <user@example.com>\n'
        'To: <someone_else@example.com>\n'
        'Subject: Test message\n'
        '\n'
        'Body would go here\n')

#  Now the header items can be accessed as a dictionary:
print(f"To: {headers['to']}")
print(f"From: {headers['from']}")
print(f"Subject: {headers['subject']}")

# You can also access the parts of the addresses:
print(f"Recipient username: {headers['to'].addresses[0].username}")
print(f"Sender name: {headers['from'].addresses[0].display_name}")
