from bottle import post, request, response
from services.validator_user import *
from services.credentials import  gmail_address ,gmail_password
from services.email import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import uuid
import time
import json
import re
import smtplib, ssl

##################################################
@post('/api/tweets')
def _():
    # VALIDATE
    # First name
    if not request.forms.get('first-name'):
        response.status = 400
        return "first-name is missing"
    if len(request.forms.get('first-name').strip()) < NAME_MIN_LEN:
        response.status = 400
        return f"first-name must contain more than {NAME_MIN_LEN} characters"
    if len(request.forms.get('first-name').strip()) > NAME_MAX_LEN:
        response.status = 400
        return f"first-name must contain less than {NAME_MAX_LEN} characters"
    if not re.match(NAME_REGEX, request.forms.get('first-name').strip()):
        response.status = 400
        return "first-name should contain only letters, start with uppercase and continue with lowercase letters"
    # Middle name
    if request.forms.get('middle-name'):
        if len(request.forms.get('middle-name').strip()) < NAME_MIN_LEN:
            response.status = 400
            return f"middle-name must contain more than {NAME_MIN_LEN} characters"
        if len(request.forms.get('middle-name').strip()) > NAME_MAX_LEN:
            response.status = 400
            return f"middle-name must contain less than {NAME_MAX_LEN} characters"       
        if not re.match(NAME_REGEX, request.forms.get('middle-name').strip()):
            response.status = 400
            return "first-name should contain only letters, start with uppercase and continue with lowercase letters"
    # Last name
    if not request.forms.get('last-name'):
        response.status = 400
        return "last-name is missing"
    if len(request.forms.get('last-name').strip()) < NAME_MIN_LEN:
        response.status = 400
        return f"last-name must contain more that {NAME_MIN_LEN} characters"
    if len(request.forms.get('last-name').strip()) > NAME_MAX_LEN:
        response.status = 400
        return f"last-name must contain less than {NAME_MAX_LEN} characters"
    if not re.match(NAME_REGEX, request.forms.get('last-name').strip()):
        response.status = 400
        return f"last-name should contain only letters, start with uppercase and continue with lowercase letters"
    # # Address
    if not request.forms.get('address'):
        response.status = 400
        return "address is missing"
    if len(request.forms.get('address').strip()) < ADDRESS_MIN_LEN:
        response.status = 400
        return f"address must contain more than {ADDRESS_MIN_LEN} characters"
    if len(request.forms.get('address').strip()) > ADDRESS_MAX_LEN:
        response.status = 400
        return "address must contain more than {ADDRESS_MAX_LEN} characters"
    if not re.match(ADDRESS_REGEX, request.forms.get('address').strip()):
        response.status = 400
        return """address is not in right format. right format is Amager Boulevard 23, 
            Amager Strand Vej 14 A, Amager Strand Vej 144, Amager Strand Vej 144 a"""
    # Age
    if not request.forms.get('age'):
        response.status = 400
        return "age is missing"
    if not re.match(AGE_REGEX, request.forms.get('age').strip()):
        response.status = 400
        return f"age must be a number between {AGE_MIN} and {AGE_MAX}"
    if int(request.forms.get('age').strip()) < AGE_MIN:
        response.status = 400
        return f"user must be {AGE_MIN} or more years old"
    if int(request.forms.get('age').strip()) > AGE_MAX:
        response.status = 400
        return "?????"
    # Username
    if not request.forms.get('username'):
        response.status = 400
        return "username is missing"
    if len(request.forms.get('username').strip()) < USERNAME_MIN_LENGTH:
        response.status = 400
        return f"userame must contain more than {USERNAME_MIN_LENGTH} characters"
    if len(request.forms.get('username').strip()) > USERNAME_MAX_LENGHT:
        response.status = 400
        return f"username must contain less than {USERNAME_MAX_LENGHT} characters"
    if not re.match(USERNAME_REGEX, request.forms.get('username').strip()):
        response.status = 400
        return """username is not in right format. right format is Big_Green cucumber11,
            BigGreencucumber11, big_green_cucumber11, big_green_cucumber"""
    # Email
    if not request.forms.get('email'):
        response.status = 400
        return "email is missing"
    if len(request.forms.get('email').strip()) < EMAIL_MIN_LEN:
        response.status = 400
        return f"email must contain at least {EMAIL_MIN_LEN} characters"
    if len(request.forms.get('email').strip()) > EMAIL_MAX_LEN:
        response.status = 400
        return f"email must contain less than {EMAIL_MAX_LEN} characters"
    if not re.match(EMAIL_REGEX, request.forms.get('email').strip()):
        response.status = 400
        return """email is not in right format. right format is johnybravo@gmail.com johnybravo@hotmail.com
            johnybravo@stud.kea.dk johnybravo23@gmail.com johny.bravo@gmail.com johny_bravo@gmail.com"""
    # Password
    if not request.forms.get('password'):
        response.status = 400
        return "password is missing"
    if not re.match(PASSWORD_REGEX, request.forms.get('password').strip()):
        response.status = 400
        return "password can only contain uppercase and lowecase characters, numbers and special symbols like #, ! and $"
    if len(request.forms.get('password').strip()) < PASSWORD_MIN_LEN:
        response.status = 400
        return f"password must contain at least {PASSWORD_MIN_LEN} characters"
    if len(request.forms.get('password').strip()) > PASSWORD_MAX_LEN:
        response.status = 400
        return f"password must contain at least {PASSWORD_MAX_LEN} characters"
    # Password-retype
    if not request.forms.get('password-retype'):
        response.status = 400
        return "password-retype is missing"
    if not re.match(PASSWORD_REGEX, request.forms.get('password-retype').strip()):
        response.status = 400
        return "password-retype can only contain uppercase and lowecase characters, numbers and special symbols like #, ! and $"
    if len(request.forms.get('password-retype').strip()) < PASSWORD_MIN_LEN:
        response.status = 400
        return f"password-retype must contain at least {PASSWORD_MIN_LEN} characters"
    if len(request.forms.get('password-retype').strip()) > PASSWORD_MAX_LEN:
        response.status = 400
        return f"password-retype must contain at least {PASSWORD_MAX_LEN} characters"
    # Password and password retype not matching
    if not request.forms.get('password') == request.forms.get('password-retype'):
        response.status = 400
        return f"password and password-retype are not matching"
    # GET DATA FROM FORM AND CREATE USER DICTIONARY
    user_id = str(uuid.uuid4())
    user_first_name = request.forms.get('first-name')
    user_middle_name = request.forms.get('middle-name') or ''
    user_last_name = request.forms.get('last-name')
    user_address = request.forms.get('address')
    user_age = request.forms.get('age')
    user_username = request.forms.get('username')
    user_email = request.forms.get('email')
    user_password = request.forms.get('password')
    # Create user dictionary
    user = {
        'user_id': user_id,
        'user_first_name': user_first_name,
        'user_middle_name': user_middle_name,
        'user_last_name': user_last_name,
        'user_address': user_address,
        'user_age': user_age,
        'user_username': user_username,
        'user_email': user_email,
        'user_password': user_password,
        'user_role': 'user'
    }
    try:
        # Connect to database
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit()
        # Insert new user
        counter = connection.execute("""
            INSERT INTO users
            VALUES (:user_id, :user_first_name, :user_middle_name, :user_last_name, :user_address, 
                :user_age, :user_username, :user_email, :user_password, :user_role)
        """, user).rowcount
        connection.commit()
        if not counter:
            print("No user has been inserted.")
            exit()
        print(f"User has been inserted.")
    except Exception as exception:
        response.status = 500
        print("Exception", exception)
        data = {
            "userAdded": False,
            "emailSent": False
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # ON SUCCESS, SEND EMAIL AND RETURN DATA
    # Get gmail credentials
    sender_email = gmail_address
    receiver_email = user_email
    password = gmail_password

    # Create mail header
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Welcome to Twitter'
    message['From'] = sender_email 
    message['To'] = receiver_email

    # Create mail body
    plaintext_mail = build_plaintext_mail()
    html_mail = build_html_mail()
    part_1 = MIMEText(plaintext_mail, 'plain')
    part_2 = MIMEText(html_mail, 'html')
    message.attach(part_1)
    message.attach(part_2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    print(sender_email)
    print(password)
    print(receiver_email)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            email_sent = True
        except Exception as exception:
            email_sent = False
            print(exception)
    # Success
    response.status = 200
    data = {
        "userAdded": True,
        "emailSent": email_sent
    }
    dataJSON = json.dumps(data)
    # Return JSON   
    return dataJSON