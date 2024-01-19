import imaplib
import email
import re

def fetch_emails():
    delayed_tickets= {}
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

# Login to the email account
    mail.login('ziakhanalone100@gmail.com', 'yyeh ynej hqar dlbm ')

    # Select the inbox
    mail.select("inbox")

    # Search for emails from reservations@piac.aero
    result, data = mail.search(None, 'FROM', 'reservations@piac.aero', 'SUBJECT', 'PNR*')

    # Loop over the email numbers
    for num in data[0].split():
    # Fetch the email data
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]

        # Parse the email
        email_message = email.message_from_bytes(raw_email)

        # Check if the email has the "PNR" word in the body
        email_body = email_message.get_payload()[0].get_payload()
        if 'PNR' in email_body:
            # Extract the PNR value
            pnr_match = re.search(r'PNR\*([A-Z0-9]+)', email_body)
            if pnr_match:
                pnr = pnr_match.group(1)

                # Extract the date and time
                datetime_match = re.search(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})', email_body)
                if datetime_match:
                    datetime = datetime_match.group(1)
                delayed_tickets.append((pnr, datetime))
        else:
            print("Email does not contain PNR")

# Close the connection
    mail.logout()
    
