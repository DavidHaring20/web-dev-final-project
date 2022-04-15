from bottle import delete, response
import sqlite3
import time
import json

##################################################
@delete('/api/sessions/<user_id>')
def _(user_id):
    # VALIDATE
    if not user_id:
        response.status = 400
        return "user_id is missing"
    # Create filter
    filter = {
        "user_id": user_id
    }
    # DELETE SESSION BY USER ID
    try:
        connection = sqlite3.connect('twitter.db')
        if not connection:
            print("The connection couldn't be established.")
            exit()
        counter = connection.execute("""
            DELETE FROM sessions_users
            WHERE
                user_id = :user_id
        """, filter).rowcount
        connection.commit()
        if not counter:
            response.status = 404
            print("Something went wrong in logging out. Couldn't find session.")
            data = {
                "logout": False
            }
            dataJSON = json.dumps(data)
            return dataJSON
        print("Logged out.")
    except Exception as exception:
        response.status = 500
        print("Exception", exception)
    finally:
        connection.close()
    time.sleep(1)
    # Success
    data = {
        "logout": True
    }
    dataJSON = json.dumps(data)
    return dataJSON
    
