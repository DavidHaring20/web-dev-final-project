from bottle import get, response
from services.dictionary_factory import dictionary_factory, dictionary_factory_JSON
from services.validator_tweet import USER_ID_REGEX, USER_ID_LEN
import sqlite3
import time
import json
import re

##################################################
@get('/api/tweets/user/<user_id>')
def _(user_id):
    # VALIDATE
    if not user_id:
        response.status = 400
        return "user_id is missing"
    if not re.match(USER_ID_REGEX, user_id):
        response.status = 400
        return "user-id should contain only characters, digits and hyphens(-)"
    if not len(user_id) == USER_ID_LEN:
        response.status = 400
        return f"user-id should have {USER_ID_LEN} characters"
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
        # Get tweets from user and from followed users
        tweets = connection.execute("""
            SELECT * FROM tweets
            LEFT JOIN users ON 
                users.user_id = tweets.user_id
            WHERE users.user_id = :user_id OR 
                users.user_id IN (
                    SELECT followed_user_id
                    FROM follows
                    WHERE follower_user_id = :user_id
                )
            ORDER BY 
                tweet_updated_at DESC,
                tweet_created_at DESC
        """, filter).fetchall()
        # Check if tweets are found
        if not tweets:
            response.status = 404
            data = {
                "tweetsFound": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("Tweets found.")
        # Get all likes relevant for user and followed user tweets
        likeSums = connection.execute("""
            SELECT *  
            FROM likes
            WHERE likes.user_id = :user_id OR
                likes.user_id = (
                    SELECT follower_user_id
                    FROM follows
                    WHERE followed_user_id = :user_id
                )
            """, filter).fetchall()
        print("Likes", likeSums)
    except Exception as exception:
        response.status = 500
        print("Exception", exception) 
    finally:
        connection.close()
    time.sleep(2)
    # Traverse tweets and add likes to tweets
    if likeSums:
        for tweet in tweets:
            tweet['likes'] = 0
            tweet['liked'] = False
            for like in likeSums:
                if like['tweetId'] == tweet['tweetId']:
                    tweet['likes'] += 1
                    if like['userId'] == user_id:
                        tweet['liked'] = True
    data = {
        "tweetsFound": True,
        "numberOfTweets": len(tweets),
        "tweets": tweets
    }
    dataJSON = json.dumps(data)
    return dataJSON
