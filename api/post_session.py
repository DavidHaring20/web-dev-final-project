from bottle import post, request, response
from services.validator_user import EMAIL_REGEX, EMAIL_MAX_LEN, EMAIL_MIN_LEN, PASSWORD_REGEX, PASSWORD_MIN_LEN, PASSWORD_MAX_LEN
from services.credentials import secret_key
import re
import time
import sqlite3
import json
import jwt

##################################################
@post('/api/sessions')
def _():
    # VALIDATION
    # Email
    if not request.forms.get('email'):
        response.status = 400
        return {"errorMessage": "Email is missing"}
    if len(request.forms.get('email').strip()) < EMAIL_MIN_LEN:
        response.status = 400
        return {"errorMessage": f"Email must contain at least {EMAIL_MIN_LEN} characters"}
    if len(request.forms.get('email').strip()) > EMAIL_MAX_LEN:
        response.status = 400
        return {"errorMessage": f"Email must contain less than {EMAIL_MAX_LEN} characters"}
    if not re.match(EMAIL_REGEX, request.forms.get('email').strip()):
        response.status = 400
        return {"errorMessage": "Email is not in right format. right format is johnybravo@gmail.com johnybravo@hotmail.com, johnybravo@stud.kea.dk johnybravo23@gmail.com johny.bravo@gmail.com johny_bravo@gmail.com"}
    # Password
    if not request.forms.get('password'):
        response.status = 400
        return {"errorMessage": "Password is missing"}
    if not re.match(PASSWORD_REGEX, request.forms.get('password').strip()):
        response.status = 400
        return {"errorMessage": "Password can only contain uppercase and lowecase characters, numbers and special symbols like #, ! and $"}
    if len(request.forms.get('password').strip()) < PASSWORD_MIN_LEN:
        response.status = 400
        return {"errorMessage": f"Password must contain at least {PASSWORD_MIN_LEN} characters"}
    if len(request.forms.get('password').strip()) > PASSWORD_MAX_LEN:
        response.status = 400
        return {"errorMessage": f"Password must contain at least {PASSWORD_MAX_LEN} characters"}
    # Get data 
    email = request.forms.get('email')
    password = request.forms.get('password')
    filter = {
        'email': email,
        'password': password
    }
    # CHECK IF THE USER EXISTS
    try:
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit()
        # Get user with email and password
        user = connection.execute("SELECT * FROM users WHERE user_email = :email AND user_password = :password", filter).fetchone()
        if not user:
            response.status = 404
            print("No user has been found.")
            data = {
                "login": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("User has been found.") 
        # INSERT USER INTO SESSIONS
        user_dictionary = {
            "user_id": user[0]
        }
        counter = connection.execute("INSERT INTO sessions_users(user_id) VALUES (:user_id)", user_dictionary).rowcount
        connection.commit()
        if not counter:
            response.status = 500
            print("Something went wrong in accessing the session.")
            data = {
                "login": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("User added to session.")
    except Exception as exception:
        response.status = 500
        print("Exception", exception)
    finally:
        connection.close()
    time.sleep(1)
    # Create dictionary for payload in JWT 
    payload = {
        'user_id': user[0],
        'user_username': user[6],
        'user_email': user[7]
    }
    print(user)
    # Create cookie with JWT
    jwt_encoded = jwt.encode(payload, secret_key)
    response.set_cookie('jwt', jwt_encoded)
    # Success
    data = {
        "userId": user[0],
        "userName": user[1],
        "userSurname": user[3],
        "userUsername": f"@{user[6]}",
        "login": True
    }
    dataJSON = json.dumps(data)
    # Return JSON
    return dataJSON