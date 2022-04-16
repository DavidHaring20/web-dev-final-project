from bottle import delete, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3
import time
import json
import re

##################################################
@delete('/api/sessions/<user_id>')
def _(user_id):
    # VALIDATE
    # User Id
    if not user_id:
        response.status = 400
        return "user_id is missing"
    if not re.match(USER_ID_REGEX, user_id):
        response.status = 400
        return "user-id should contain only characters, digits and hyphens(-)"
    if not len(user_id) == USER_ID_LEN:
        response.status = 400
        return f"user-id should have {USER_ID_LEN} characters"
    # Create filter
    filter = {
        "user_id": user_id
    }
    # DELETE SESSION BY USER ID
    try:
        connection = sqlite3.connect('twitter.db')
        if not connection:
            print("The connection couldn't be established.")
            exit()
        counter = connection.execute("""
            DELETE FROM sessions_users
            WHERE
                user_id = :user_id
        """, filter).rowcount
        connection.commit()
        if not counter:
            response.status = 404
            print("Something went wrong in logging out. Couldn't find session.")
            data = {
                "logout": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("Logged out.")
    except Exception as exception:
        response.status = 500
        print("Exception", exception)
    finally:
        connection.close()
    time.sleep(1)
    # Success
    response.delete_cookie("jwt")
    data = {
        "logout": True
    }
    dataJSON = json.dumps(data)
    return dataJSON
    
