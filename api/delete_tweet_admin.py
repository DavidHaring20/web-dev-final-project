from bottle import delete, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN, TWEET_ID_REGEX
from services.dictionary_factory import dictionary_factory
import sqlite3
import time
import json
import re

##################################################
@delete('/api/tweets/admin/<user_id>/tweet/<tweet_id>')
def _(user_id, tweet_id):
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
    # GET USER FOR USER ROLE
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
        # DELETE TWEET
        counter = connection.execute("""
            DELETE FROM tweets
            WHERE 
                tweet_id = ?
        """, (tweet_id)).rowcount
        # Check if the tweet is deleted
        if not counter:
            # Failure
            response.status = 404
            print("Something went wrong. Couldn't find tweet.")
            data = {
                'tweetDeleted': False
            }
            dataJSON = json.dumps(data)
            return data
        # Success
        connection.commit()
        print("Tweet deleted.")
    except Exception as exception:
        response.status = 500
        data = {
            'tweetDeleted': False,
            'exception': str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        'tweetDeleted': True,
        'tweetId': tweet_id
    }
    dataJSON = json.dumps(data)
    return dataJSON