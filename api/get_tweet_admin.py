from bottle import get, response
from services.dictionary_factory import dictionary_factory, dictionary_factory_JSON
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3
import time
import json
import re

##################################################
@get('/api/tweets/admin/<user_id>')
def _(user_id):
    # VALIDATION 
    # user_id
    if not user_id:
        response.status = 400
        return "user-id is missing"
    if not re.match(USER_ID_REGEX, user_id):
        response.status = 400
        return "user-id should contain only characters, digits and hyphens(-)"
    if not len(user_id) == USER_ID_LEN:
        response.status = 400
        return f"user-id should have {USER_ID_LEN} characters"
    # GET USER FOR USER ROLE
    # GET ALL TWEETS
    try:
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit()
        # Set custom dictionary factory 
        connection.row_factory = dictionary_factory
        user = connection.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not user:
            # Failure to find user
            response.status = 404
            print("No user found.")
            data = {
                "userFound": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # Success to find user
        # Check user role
        if 'user_role' in user:
            if user['user_role'] != 'admin':
                # Failure
                response.status = 401
                print("Access restricted.")
                data = {
                    "accessRestricted": True
                }
                dataJSON = json.dumps(data)
                return dataJSON
        # Set custom dictionary factory 
        connection.row_factory = dictionary_factory_JSON
        # Get tweet
        tweets = connection.execute("SELECT * FROM tweets").fetchall()
        if not tweets:
            # Failure
            response.status = 500
            print("No tweets found.")
            data = {
                "tweetsFound": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # Success
        print("Tweets found.")
    except Exception as exception:
        response.status = 500
        data = {
            "tweetsFound": False,
            "exception": str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        "tweetsFound": True,
        "tweets": tweets
    }
    dataJSON = json.dumps(data)
    return dataJSON

