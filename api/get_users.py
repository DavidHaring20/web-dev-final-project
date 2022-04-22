from bottle import get, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
from services.dictionary_factory import dictionary_factory_JSON
from random import randint
import sqlite3
import time
import json
import re

##################################################
@get('/api/users/<user_id>')
def _(user_id):
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
    # Create dictionary
    user = {
        "user_id": user_id
    }
    # Get users
    try:
        # Connect to the database
        connection = sqlite3.connect('twitter.db')
        # Test the connection
        if not connection:
            print("Connection couldn't be established.")
            exit()
        # Assign custom dictionary which is JSON friendly
        connection.row_factory = dictionary_factory_JSON
        # Get all users that user is following
        all_users_not_followed = connection.execute("""
            SELECT * FROM users
            WHERE NOT user_id = :user_id AND  
                users.user_id NOT IN (
                    SELECT followed_user_id 
                    FROM follows
                    WHERE 
                        follower_user_id = :user_id
                    )
        """, user).fetchall()
        # Get all users that user is not following
        all_users_followed = connection.execute("""
            SELECT * FROM follows
            LEFT JOIN users ON
                follows.followed_user_id = users.user_id
            WHERE
                follows.follower_user_id = ?
        """, (user_id,)).fetchall()
        # Get number of tweets written by each user
        tweets_count = connection.execute("""
            SELECT user_id, COUNT(*) FROM tweets
            GROUP BY user_id
        """).fetchall()
    except Exception as exception:
        response.status = 500
        data = {
            "usersGet": False,
            "exception": str(exception)
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    # Take five random users from the list that the user is not following
    # If there are less than 5 users in the db, then take all of them
    if all_users_not_followed and all_users_followed:
        users_not_followed = []
        if len(all_users_not_followed) < 5:
            users_not_followed = all_users_not_followed
        # Integers will store numbers that have been created already, what 
        # cancels the option to have duplicate users in the follow tab
        integers = []
        for i in range(0, 5, 1):
            random = randint(0, len(all_users_not_followed) - 1)
            while random in integers:
                random = randint(0, len(all_users_not_followed) - 1)
            integers.append(random)
            users_not_followed.append(all_users_not_followed[random])
        for tweetCount in tweets_count:
            for user in users_not_followed:
                if tweetCount['userId'] == user['userId']:
                    user['tweetAmount'] = tweetCount['COUNT(*)']
        # Add number of tweets written to the users that are in the final list
        data = {
            "usersGet": True,
            "numberOfAllUsersNotFollowed": len(all_users_not_followed),
            "numberOfUsersNotFollowed": len(users_not_followed),
            "numberOfUsersFollowed": len(all_users_followed),
            "usersNotFollowed": users_not_followed,
            "usersFollowed": all_users_followed
        }
        dataJSON = json.dumps(data)
        return dataJSON
    return "nothing"
