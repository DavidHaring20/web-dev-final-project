from faker import Faker
import sqlite3
import time
import random

fake = Faker()

##################################################
def removeTuples(listOfTuples):
    list = []
    for tuple in listOfTuples:
        user_id = tuple[0]
        list.append(user_id)
    return list

##################################################
def createFakeTweets(user_ids):
    tweets = [
        {
            "tweet_title": fake.sentence(nb_words=6, variable_nb_words=True), 
            "tweet_description": fake.paragraph(nb_sentences=4, variable_nb_sentences=True),
            "tweet_image_url": f"/images/{fake.word()}_{fake.word()}.{fake.file_extension(category='image')}",
            "tweet_created_at": f"{fake.day_of_month()} {fake.month()} 2022 {fake.time()}",
            "tweet_updated_at": f"{fake.day_of_month()} {fake.month()} 2022 {fake.time()}",
            "user_id": random.choice(user_ids),
        } for i in range(20)
    ]
    return tweets

##################################################
# Connect to the database and get all user_id-s (they are needed to insert tweets)
try:
    connection = sqlite3.connect('../twitter.db')
    user_ids = connection.execute("SELECT user_id FROM users").fetchall()
    if not user_ids:
        print("No user_id-s found.")
        exit()
    user_ids = removeTuples(user_ids)
    # Use user_id-s to generate tweets that belong to them
    tweets = createFakeTweets(user_ids)
    counter = connection.executemany("""
        INSERT INTO tweets (tweet_title, tweet_description, tweet_image_url, tweet_created_at, tweet_updated_at, user_id)
        VALUES (:tweet_title, :tweet_description, :tweet_image_url, :tweet_created_at, :tweet_updated_at, :user_id)
    """, tweets).rowcount
    connection.commit()
    if not counter:
        print("Something went wrong. No tweets were inserted.") 
        exit()
    print(f"Number of tweets inserted: {counter}")
except Exception as exception:
    print(exception)
finally:
    connection.close()
time.sleep(2)




