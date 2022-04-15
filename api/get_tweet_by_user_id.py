from bottle import get, response
from services.dictionary_factory import dictionary_factory_JSON
import sqlite3
import time
import json

##################################################
@get('/api/tweets/user/<user_id>')
def _(user_id):
    # VALIDATE
    if not user_id:
        response.status = 400
        return "user_id is missing"
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
