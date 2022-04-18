from bottle import post, request, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3
import time
import re
import json

##################################################
@post('/api/follows')
def _():
    # VALIDATION
    # follower_user_id
    if not request.forms.get('follower_user_id'):
        response.status = 400
        return "follower_user_id is missing"
    if not re.match(USER_ID_REGEX, request.forms.get('follower_user_id').strip()):
        response.status = 400
        return "follower_user_id should contain only characters, digits and hyphens(-)"
    if not len(request.forms.get('follower_user_id').strip()) == USER_ID_LEN:
        response.status = 400
        return f"follower_user_id should have {USER_ID_LEN} characters"
    # followed_user_id
    if not request.forms.get('followed_user_id'):
        response.status = 400
        return "followed_user_id is missing"
    if not re.match(USER_ID_REGEX, request.forms.get('followed_user_id').strip()):
        response.status = 400
        return "followed_user_id should contain only characters, digits and hyphens(-)"
    if not len(request.forms.get('followed_user_id').strip()) == USER_ID_LEN:
        response.status = 400
        return f"followed_user_id should have {USER_ID_LEN} characters"
    # follower_user_id and followed_user_id can't be same as one user can't follow itself
    if request.forms.get('follower_user_id') == request.forms.get('followed_user_id'):
        response.status = 400
        return f"follower_user_id and followed_user_id can't be same"
    
    # Get data from form
    follower_user_id = request.forms.get('follower_user_id')
    followed_user_id = request.forms.get('followed_user_id')
    # Create follow dictionary
    follow = {
        "follower_user_id": follower_user_id,
        "followed_user_id": followed_user_id
    }
    print(follow)
    # INSERT FOLLOW
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
            INSERT INTO follows
            VALUES(:follower_user_id, :followed_user_id)
        """, follow).rowcount
        # Check if follow was inserted 
        if not counter:
            # Failure
            response.status = 500
            print("Something went wrong in inserting the follow.")
            data = {
                "followed": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # Success
        connection.commit()
        print("Followed.")
    except Exception as exception:
        response.status = 500
        data = {
            "followed": False,
            "exception": str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        "followed": True
    }
    dataJSON = json.dumps(data)
    return dataJSON