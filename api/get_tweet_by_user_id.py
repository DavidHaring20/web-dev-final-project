from bottle import get, response
from services.dictionary_factory import dictionary_factory_JSON
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3
import time
import json
import re

##################################################
@get('/api/tweets/user/<user_id>')
def _(user_id):
    # VALIDATE
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
    # GET ALL USER TWEETS
    # Create connection
    try:
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit()
        # Set custom dictionary factory
        connection.row_factory = dictionary_factory_JSON
        # Get tweets from user
        tweets = connection.execute("""
            SELECT * FROM tweets
            WHERE 
                user_id = :user_id
        """, filter).fetchall()
        if not tweets:
            response.status = 404
            data = {
                "tweetsFound": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("Tweets found.")
    except Exception as exception:
        response.status = 500
        print("Exception", exception) 
    finally:
        connection.close()
    time.sleep(1)
    print(tweets)
    data = {
        "tweetsFound": True,
        "tweets": tweets
    }
    dataJSON = json.dumps(data)
    return dataJSON