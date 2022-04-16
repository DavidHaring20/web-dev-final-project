from bottle import post, request, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN, TWEET_ID_REGEX
import re
import sqlite3 
import time
import json


##################################################
@post('/api/likes')
def _():
    # VALIDATION
    # user_id
    if not request.forms.get('user_id'):
        response.status = 400
        return "user_id is missing"
    if not re.match(USER_ID_REGEX, request.forms.get('user_id').strip()):
        response.status = 400
        return "user_id should contain only characters, digits and hyphens(-)"
    if not len(request.forms.get('user_id').strip()) == USER_ID_LEN:
        response.status = 400
        return f"user_id should have {USER_ID_LEN} characters"
    # tweet_id
    if not request.forms.get('tweet_id'):
        response.status = 400
        return "tweet_id is missing"
    if not re.match(TWEET_ID_REGEX, request.forms.get('tweet_id')):
        response.status = 400
        return "tweet id must be a positive number and can contain only integers"
    if not int(request.forms.get('tweet_id')) > 0:
        response.status = 400
        return "tweet id must be a positive number"
    # Get data from form
    tweet_id = request.forms.get('tweet_id')
    user_id = request.forms.get('user_id')
    # Create like
    like = {
        'tweet_id': tweet_id,
        'user_id': user_id
    }
    # INSERT LIKE
    try:
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit() 
        # Turn on foreign key check
        connection.execute("PRAGMA foreign_keys = ON")
        # Insert into the database
        counter = connection.execute("""
            INSERT INTO likes
            VALUES(:tweet_id, :user_id)
        """, like).rowcount
        connection.commit()
        # Failure
        if not counter:
            response.status = 500
            print("Something went wrong in inserting the like.")
            data = {
                "liked": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # Success 
        print("Liked.")
    except Exception as exception:
        response.status = 500
        print('Exception', exception)
        data = {
            "liked": False,
            "exception": str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        "liked": True
    }
    dataJSON = json.dumps(data)
    return dataJSON