from bottle import run, static_file, get

##################################################
# Api
import api.post_user
import api.post_session
import api.delete_session
import api.get_tweet_by_tweet_id
import api.get_tweet_by_user_id
import api.post_tweet
import api.delete_tweet

##################################################
@get('/app.css')
def _():
    return static_file('app.css', root='./stylesheets')

@get('/app.js')
def _():
    return static_file('app.js', root='.')

@get('/images/<image_name>')
def _(image_name):
    return static_file(image_name, root='./images')

##################################################
run(host='localhost', port='8080', reloader=True, debug=True)
