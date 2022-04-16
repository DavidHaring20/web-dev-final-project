from bottle import get, response
from services.dictionary_factory import dictionary_factory_JSON
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN, TWEET_ID_REGEX
import sqlite3
import time
import json
import re

##################################################
@get('/api/tweets/user/<user_id>/tweet/<tweet_id>')
def _(user_id ,tweet_id):
    # VALIDATION
    # user_id
    if not user_id:
        response.status = 400
        return "user_id is missing"
    if not re.match(USER_ID_REGEX, user_id):
        response.status = 400
        return "user-id should contain only characters, digits and hyphens(-)"
    if not len(user_id) == USER_ID_LEN:
        response.status = 400
        return f"user-id should have {USER_ID_LEN} characters"
    # tweet_id
    if not tweet_id:
        response.status = 400
        return "tweet_id is missing"
    if not re.match(TWEET_ID_REGEX, tweet_id):
        response.status = 400
        return "tweet id must be a positive number and can contain only integers"
    if not int(tweet_id) > 0:
        response.status = 400
        return "tweet id must be a positive number"
    # Create filter
    filter = {
        "user_id": user_id,
        "tweet_id": tweet_id
    }
    # GET TWEET WITH USER ID AND TWEET ID
    # Connect to database
    try:
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit()
        # Set custom dictionary factory 
        connection.row_factory = dictionary_factory_JSON
        # Get tweet
        tweet = connection.execute("""
            SELECT * FROM tweets
            WHERE 
                tweet_id = :tweet_id AND
                user_id = :user_id
        """, filter).fetchone()
        if not tweet:
            response.status = 404
            data = {
                "tweetFound": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("Tweet found.")
    except Exception as exception:
        response.status = 500
        print("Exception",exception)
    finally:
        connection.close()
    time.sleep(1)
    print(tweet)
    data = {
        "tweetFound": True,
        "tweet": tweet
    }
    dataJSON = json.dumps(data)
    return dataJSON
