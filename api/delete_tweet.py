from bottle import delete, request, response
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN, TWEET_ID_REGEX
from services.dictionary_factory import dictionary_factory
from services.directories import IMAGES_DIRECTORY
import os
import sqlite3 
import time
import json
import re

##################################################
@delete('/api/tweets/user/<user_id>/tweet/<tweet_id>')
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
    # Create filter for deleting tweet
    filter = {
        'tweet_id': tweet_id,
        'user_id': user_id
    }
    # GET TWEET_IMAGE_URL FROM USER BY TWEET ID AND USER ID
    # DELETE TWEET BY TWEET ID AND USER ID
    try:
        # Create a connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection coudln't be established.")
            exit()
        # Use custom dictionary factory
        connection.row_factory = dictionary_factory
        # Get image name
        tweet = connection.execute("""
            SELECT * FROM tweets
            WHERE 
                tweet_id = :tweet_id AND
                user_id = :user_id
        """, filter).fetchone()
        if not tweet:
            response.status = 404
            print("Something went wrong. Couldn't find tweet.")
            data = {
                'tweetDeleted': False
            }
            dataJSON = json.dumps(data)
            return data
        print(tweet)
        image_name = tweet['tweet_image_url']
        # Delete tweet
        counter = connection.execute("""
            DELETE FROM tweets
            WHERE 
                tweet_id = :tweet_id AND 
                user_id = :user_id
        """, filter).rowcount
        connection.commit()
        # Check if the tweet is deleted
        if not counter:
            response.status = 404
            print("Something went wrong. Couldn't find tweet.")
            data = {
                'tweetDeleted': False
            }
            dataJSON = json.dumps(data)
            return data
        # If tweet is deleted, also delete the image that belonged to it
        if os.path.exists(f"{IMAGES_DIRECTORY}/{image_name}"):
            os.remove(f"{IMAGES_DIRECTORY}/{image_name}")
            print("Tweet's image deleted.")
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
