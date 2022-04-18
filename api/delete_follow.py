from bottle import delete, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3
import time
import re
import json

##################################################
@delete('/api/follows/follower_user_id/<follower_user_id>/followed_user_id/<followed_user_id>')
def _(follower_user_id, followed_user_id):
    # VALIDATION
    # follower_user_id
    if not follower_user_id:
        response.status = 400
        return "follower_user_id is missing"
    if not re.match(USER_ID_REGEX, follower_user_id.strip()):
        response.status = 400
        return "follower_user_id should contain only characters, digits and hyphens(-)"
    if not len(follower_user_id.strip()) == USER_ID_LEN:
        response.status = 400
        return f"follower_user_id should have {USER_ID_LEN} characters"
    # followed_user_id
    if not followed_user_id:
        response.status = 400
        return "followed_user_id is missing"
    if not re.match(USER_ID_REGEX, followed_user_id.strip()):
        response.status = 400
        return "followed_user_id should contain only characters, digits and hyphens(-)"
    if not len(followed_user_id.strip()) == USER_ID_LEN:
        response.status = 400
        return f"followed_user_id should have {USER_ID_LEN} characters"
    # Create filter 
    filter = {
        "follower_user_id": follower_user_id,
        "followed_user_id": followed_user_id
    }
    # DELETE FOLLOW
    try: 
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit()
        counter = connection.execute("""
            DELETE FROM follows
            WHERE
                follower_user_id = :follower_user_id AND
                followed_user_id = :followed_user_id
        """, filter).rowcount
        # Check if follow was inserted 
        if not counter:
            # Failure
            response.status = 500
            print("Something went wrong in deleting the follow.")
            data = {
                "unfollowed": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # Success
        connection.commit()
        print("Followed.")
    except Exception as exception:
        response.status = 500
        data = {
            "unfollowed": False,
            "exception": str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        "unfollowed": True
    }
    dataJSON = json.dumps(data)
    return dataJSON