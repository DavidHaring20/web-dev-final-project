from bottle import delete, request, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3 
import time
import json
import re

##################################################
@delete('/api/tweets/<tweet_id>')
def _(tweet_id):
    # VALIDATION
    # Tweet Id
    if not tweet_id:
        response.status = 400
        return "tweet_id is missing"
    # User Id
    if not request.forms.get('user-id'):
        response.status = 400
        return "user-id is missing"
    if not re.match(USER_ID_REGEX, request.forms.get('user-id').strip()):
        response.status = 400
        return "user-id should contain only characters, digits and hyphens(-)"
    if not len(request.forms.get('user-id').strip()) == USER_ID_LEN:
        response.status = 400
        return f"user-id should have {USER_ID_LEN} characters"
    # Get data from form
    user_id = request.forms.get('user-id')
    # Create filter for deleting tweet
    filter = {
        'tweet_id': tweet_id,
        'user_id': user_id
    }
    # DELETE TWEET BY TWEET ID AND USER ID
    try:
        # Create a connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection coudln't be established.")
            exit()
        counter = connection.execute("""
            DELETE FROM tweets
            WHERE 
                tweet_id = :tweet_id AND 
                user_id = :user_id
        """, filter).rowcount
        connection.commit()
        if not counter:
            response.status = 404
            print("Something went wrong. Couldn't find tweet.")
            data = {
                'tweetDeleted': False
            }
            dataJSON = json.dumps(data)
            return data
        # Suceess
        print("Tweet deleted.")
    except Exception as exception:
        response.status = 500
        print('Exception', exception)
    finally:
        connection.close()
    time.sleep(1)
    # Sucess 
    data = {
        'tweetDeleted': True,
        'tweetId': tweet_id
    }
    dataJSON = json.dumps(data)
    return dataJSON
