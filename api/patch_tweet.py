from bottle import route, request, response
from services.validator_tweet import *
from services.date import get_date_time
from services.dictionary_factory import dictionary_factory, dictionary_factory_JSON
from services.directories import IMAGES_DIRECTORY
import sqlite3
import time
import json
import uuid
import re
import imghdr 
import os

##################################################
@route('/api/tweets/<tweet_id>', method='PATCH')
def _(tweet_id):
    global counter
    pre_update_image_name = ""
    # VALIDATION
    # Tweet Id
    if not tweet_id:
        response.status = 400
        return {"errorMessage": "tweet_id is missing" }
    if not re.match(TWEET_ID_REGEX, tweet_id):
        response.status = 400
        return {"errorMessage": "tweet id must be a positive number and can contain only integers" }
    if not int(tweet_id) > 0:
        response.status = 400
        return {"errorMessage": "tweet id must be a positive number" }
    # Title
    if not request.forms.get('title'):
        response.status = 400
        return {"errorMessage": "title is missing" }
    if not re.match(TEXT_REGEX, request.forms.get('title').strip()):
        response.status = 400
        return {"errorMessage": "title can only contain letters, numbers and these symbols: \".\", \",\", \"!\", \"?\", \"'\", \"(\", \")\""}
    if len(request.forms.get('title').strip()) < TITLE_MIN_LEN:
        response.status = 400
        return {"errorMessage": f"title must contain at least {TITLE_MIN_LEN} characters"}
    if len(request.forms.get('title').strip()) > TITLE_MAX_LEN:
        response.status = 400
        return {"errorMessage": f"title must contain less than {TITLE_MAX_LEN} characters"}
    # Description
    if not request.forms.get('description'):
        response.status = 400
        return {"errorMessage": "description is missing"}
    if not re.match(TEXT_REGEX, request.forms.get('description').strip()):
        response.status = 400
        return {"errorMessage": "description can only contain letters, numbers and these symbols: \".\", \",\", \"!\", \"?\", \"'\", \"(\", \")\""}
    if len(request.forms.get('description').strip()) < DESCRIPTION_MIN_LEN:
        response.status = 400
        return {"errorMessage": f"description must contain at least {DESCRIPTION_MIN_LEN} characters"}
    if len(request.forms.get('description').strip()) > DESCRIPTION_MAX_LEN:
        response.status = 400
        return {"errorMessage": f"description must contain less than {DESCRIPTION_MAX_LEN} charaters"}
    # User Id
    if not request.forms.get('user-id'):
        response.status = 400
        return {"errorMessage": "user-id is missing"}
    if not re.match(USER_ID_REGEX, request.forms.get('user-id').strip()):
        response.status = 400
        return {"errorMessage": "user-id should contain only characters, digits and hyphens(-)"}
    if not len(request.forms.get('user-id').strip()) == USER_ID_LEN:
        response.status = 400
        return {"errorMessage": f"user-id should have {USER_ID_LEN} characters"}
    # Get data from form
    tweet_title = request.forms.get('title')
    tweet_description = request.forms.get('description')
    tweet_updated_at = get_date_time()
    user_id = request.forms.get('user-id')
    tweet = {
        'tweet_id': tweet_id,
        'tweet_title': tweet_title,
        'tweet_description': tweet_description,
        'tweet_updated_at': tweet_updated_at,
        'user_id': user_id
    }
    # Image
    if request.files.get('image'):
        # Image
        if not request.files.get('image'):
            response.status = 400
            return "image is missing"
        # Get image from form and get file_name and file_extension from image
        image = request.files.get('image')
        file_name, file_extension = os.path.splitext(image.filename)
        # File extension
        if file_extension not in IMAGE_EXTENSIONS:
            response.status = 400
            return f"file is not of type {IMAGE_EXTENSIONS}"
        # Image Name
        if not re.match(IMAGE_NAME_REGEX, file_name.strip()):
            response.status = 400
            return "image-name can contain only uppercase and lowercase letters, numbers these special characters: \".\", \"_\" and \"-\"."
        if len(file_name.strip()) < IMAGE_NAME_MIN_LEN:
            response.status = 400
            return f"image-name must contain at least {IMAGE_NAME_MIN_LEN} characters"
        if len(file_name.strip()) > IMAGE_NAME_MAX_LEN:
            response.status = 400
            return f"image-name must contain less than {IMAGE_NAME_MAX_LEN} characters"
        # Success
        # Create name for image
        image_id = str(uuid.uuid4())
        image_name = f"{image_id}{file_extension}"
        # Check if there is a directory where system will store images
        if not os.path.exists(f"/{IMAGES_DIRECTORY}"):
            os.mkdir(IMAGES_DIRECTORY)
            print(f"Created {IMAGES_DIRECTORY} directory")

        # Save image with new generated name
        print(f"{IMAGES_DIRECTORY}/{image_name}")
        image.save(f"{IMAGES_DIRECTORY}/{image_name}")
        print("Image saved.")

        # Overwrite .jpg to .jpeg so imghdr will pass validation 
        if file_extension == '.jpg':
            file_extension = '.jpeg'

        # Check the image validity
        imghdr_extension = imghdr.what(f"{IMAGES_DIRECTORY}/{image_name}")
        if file_extension != f".{imghdr_extension}":
            # Delete image
            os.remove(f"{IMAGES_DIRECTORY}/{image_name}")
            print("Image deleted due to being invalid.")        
        # Success
        tweet['tweet_image_url'] = image_name
    # UPDATE TWEET BY TWEET ID
    try:
        # Create connection
        connection = sqlite3.connect('twitter.db')
        # Test connection
        if not connection:
            print("The connection couldn't be established.")
            exit() 
        # See if the user added new photo
        if 'tweet_image_url' in tweet:
            # Use custom dictionary factory
            connection.row_factory = dictionary_factory
            # Get name of the old image
            pre_update_image = connection.execute("""
                SELECT tweet_image_url FROM tweets
                WHERE 
                    tweet_id = :tweet_id AND
                    user_id = :user_id
            """, tweet).fetchone()
            print(pre_update_image)
            if pre_update_image['tweet_image_url']:
                pre_update_image_name = pre_update_image['tweet_image_url']
            # Query with new image
            counter = connection.execute("""
            UPDATE tweets
            SET tweet_title = :tweet_title,
                tweet_description = :tweet_description,
                tweet_updated_at = :tweet_updated_at,
                tweet_image_url = :tweet_image_url
            WHERE 
                tweet_id = :tweet_id AND
                user_id = :user_id
            """, tweet).rowcount
        else: 
            # Query without image
            counter = connection.execute("""
            UPDATE tweets
            SET tweet_title = :tweet_title,
                tweet_description = :tweet_description,
                tweet_updated_at = :tweet_updated_at
            WHERE 
                tweet_id = :tweet_id AND
                user_id = :user_id
            """, tweet).rowcount
        # Commit change
        connection.commit()
        if not counter:
            response.status = 500
            print("No tweet has been updated.")
            data = {
                'tweetUpdated': False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        # On success delete old picture
        if pre_update_image_name:
            if os.path.exists(f"{IMAGES_DIRECTORY}/{pre_update_image_name}"):
                os.remove(f"{IMAGES_DIRECTORY}/{pre_update_image_name}")
                print("Tweet's old image deleted.")
        print("Tweet has been updated.")
        # Create filter for searching for new tweet
        filter = {
            'tweet_id': tweet_id,
            'user_id': user_id
        }
        # Use custom JSON-friendly dictionary_factory
        connection.row_factory = dictionary_factory_JSON
        # GET NEW TWEET 
        updated_tweet = connection.execute("""
            SELECT * FROM tweets
            WHERE 
                tweet_id = :tweet_id AND
                user_id = :user_id
        """, filter).fetchone()
        # GET USER WHOSE TWEET WAS UPDATED
        user = connection.execute("""
            SELECT * FROM users
            WHERE 
                user_id = :user_id
        """, filter).fetchone()
        if not updated_tweet:
            print("No tweet has been updated.")
            data = {
                "tweetUpdated": False          
            }
            dataJSON = json.dumps(data)
            return dataJSON
    except Exception as exception:
        response.status = 500
        print("Exception", exception)
        data = {
            "tweetUpdated": False          
        }
        dataJSON = json.dumps(data)
        return dataJSON
    finally:
        connection.close()
    time.sleep(1)
    data = {
        'tweetUpdated': True,
        'tweet': updated_tweet,
        'user': user
    }
    dataJSON = json.dumps(data)
    # Success
    return data