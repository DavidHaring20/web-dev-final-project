from bottle import delete, request, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN, TWEET_ID_REGEX
import re
import sqlite3 
import time
import json

##################################################
@delete('/api/likes/user/<user_id>/tweet/<tweet_id>')
def _(user_id, tweet_id):
    # VALIDATION
    # user_id
    if not user_id:
        response.status = 400
        return "user_id is missing"
    if not re.match(USER_ID_REGEX, user_id):
        response.status = 400
        return "user_id should contain only characters, digits and hyphens(-)"
    if not len(user_id) == USER_ID_LEN:
        response.status = 400
        return f"user_id should have {USER_ID_LEN} characters"
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
    # Create like
    like = {
        'user_id': user_id,
        'tweet_id': tweet_id
    }
    # DELETE LIKE
    try:
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit() 
        # Delete from the database
        counter = connection.execute("""
            DELETE FROM likes 
            WHERE 
                user_id = :user_id AND
                tweet_id = :tweet_id
        """, like).rowcount
        if not counter:
            # Failure
            response.status = 500
            print("Something went wrong in deleting the like.")
            data = {
                "likeDeleted": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # Success
        connection.commit()
    except Exception as exception:
        response.status = 500
        print('Exception', exception)
        data = {
            "likeDeleted": False,
            "exception": str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        "likeDeleted": True
    }
    dataJSON = json.dumps(data)
    return dataJSON
    
