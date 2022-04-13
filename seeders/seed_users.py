from faker import Faker
import uuid
import sqlite3
import time
import random

fake = Faker()

##################################################
# Create a list of users
def createFakeUsers():
    users = [
        {
            'user_id': str(uuid.uuid4()),
            'user_first_name': fake.first_name(),
            'user_middle_name': fake.first_name(),
            'user_last_name': fake.last_name(),
            'user_address': fake.address(),
            'user_age': random.randint(18, 99),
            'user_username': fake.simple_profile()['username'],
            'user_email': fake.ascii_email(),
            'user_password': fake.password(),
            'user_role': 'user',
        } for i in range(10)
    ]
    return users

##################################################
# Connect to database and insert users
try:
    connection = sqlite3.connect('../twitter.db')
    if not connection:
        print("The connection wasn't established.")
        exit()    
    counter = connection.executemany("""
        INSERT INTO users
        VALUES (:user_id, :user_first_name, :user_middle_name, :user_last_name, :user_address, 
            :user_age, :user_username, :user_email, :user_password, :user_role)
    """, createFakeUsers()).rowcount 
    connection.commit()
    if not counter: 
        print("Something went wrong. No users were inserted.")
        exit()
    print(f"Users inserted: {counter}")
except Exception as exception:
    print(exception)
finally:
    connection.close()
time.sleep(2)