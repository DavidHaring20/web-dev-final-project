from bottle import run

##################################################
# Api
import api.get_tweet_admin
import api.get_tweet_by_tweet_id
import api.get_tweet_by_user_id
import api.get_users
import api.post_user
import api.post_session
import api.post_like 
import api.post_tweet
import api.post_follow
import api.patch_tweet
import api.delete_session
import api.delete_tweet_admin
import api.delete_tweet
import api.delete_like
import api.delete_follow

##################################################
# File loaders
import loaders.html_loader
import loaders.js_loader
import loaders.css_loader
import loaders.image_loader

##################################################
run(host='localhost', port='8080', reloader=True, debug=True)
