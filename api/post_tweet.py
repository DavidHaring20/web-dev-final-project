from bottle import post, request, response
from services.validator_tweet import *
from services.date import get_date_time
from services.dictionary_factory import dictionary_factory_JSON
import sqlite3
import time
import json
import os
import re

##################################################
@post('/api/tweets')
def _():
    # VALIDATION
    # User id
    if not request.forms.get('user-id'):
        response.status = 400
        return "user-id is missing"
    if not re.match(USER_ID_REGEX, request.forms.get('user-id').strip()):
        response.status = 400
        return "user-id should contain only characters, digits and hyphens(-)"
    if not len(request.forms.get('user-id').strip()) == USER_ID_LEN:
        response.status = 400
        return f"user-id should have {USER_ID_LEN} characters"
    # Title
    if not request.forms.get('title'):
        response.status = 400
        return "title is missing"
    if not re.match(TEXT_REGEX, request.forms.get('title').strip()):
        response.status = 400
        return "title can only contain letters, numbers and these symbols: \".\", \",\", \"!\", \"?\", \"'\", \"(\", \")\""
    if len(request.forms.get('title').strip()) < TITLE_MIN_LEN:
        response.status = 400
        return f"title must contain at least {TITLE_MIN_LEN} characters"
    if len(request.forms.get('title').strip()) > TITLE_MAX_LEN:
        response.status = 400
        return f"title must contain less than {TITLE_MAX_LEN} characters"
    # Description
    if not request.forms.get('description'):
        response.status = 400
        return "description is missing"
    if not re.match(TEXT_REGEX, request.forms.get('description').strip()):
        response.status = 400
        return "description can only contain letters, numbers and these symbols: \".\", \",\", \"!\", \"?\", \"'\", \"(\", \")\""
    if len(request.forms.get('description').strip()) < DESCRIPTION_MIN_LEN:
        response.status = 400
        return f"description must contain at least {DESCRIPTION_MIN_LEN} characters"
    if len(request.forms.get('description').strip()) > DESCRIPTION_MAX_LEN:
        response.status = 400
        return f"description must contain less than {DESCRIPTION_MAX_LEN} charaters"
    # Get data from form
    tweet_title = request.forms.get('title')
    tweet_description = request.forms.get('description')
    tweet_created_at = get_date_time()
    user_id = request.forms.get('user-id')
    tweet = {
        'tweet_title': tweet_title,
        'tweet_description': tweet_description,
        'tweet_image_url': '',
        'tweet_created_at': tweet_created_at,
        'user_id': user_id,
    }
    # Image
    # if request.forms.get(''):
    #     response.status = 400
    #     return ""
    # if not re.match(, request.forms.get().strip()):
    #     response.status = 400
    #     return ""
    # if not len(request.forms.get('').strip()) <:
    #     response.status = 400
    #     return ""
    # if not len(request.forms.get('').strip()) >:
    #     response.status = 400
    #     return ""
    # INSERT NEW TWEET INTO DATABASE
    try:
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit() 
        # Insert new tweet
        counter = connection.execute("""
            INSERT INTO tweets(tweet_title, tweet_description, tweet_image_url , tweet_created_at , user_id)
            VALUES(:tweet_title, :tweet_description, :tweet_image_url, :tweet_created_at, :user_id)
        """, tweet).rowcount
        connection.commit()
        if not counter:
            print("No tweet has been inserted.")
            exit()
        print("Tweet has been inserted.")
        # Create new filter to get newly inserted tweet
        filter = {
            'user_id': user_id
        }
        # Assign custom dictionary factor to get JSON-friendly dictionary
        connection.row_factory = dictionary_factory_JSON 
        # Get new tweet
        tweet = connection.execute("""
            SELECT * FROM tweets
            WHERE 
                tweet_id = (SELECT MAX(tweet_id) FROM tweets) AND
                user_id = :user_id
        """, filter).fetchone()
        print(tweet)
        if not tweet:
            print("No tweet has been inserted.")
            data = {
                "tweetAdded": False          
            }
        print("Tweet found.")
    except Exception as exception:
        response.status = 500
        print("Exception", exception) 
    finally: 
        connection.close()
    time.sleep(1)
    data = {
        "tweetAdded": True,
        "tweet": tweet
    }
    dataJSON = json.dumps(data)
    return dataJSON