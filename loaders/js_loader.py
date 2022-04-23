from bottle import get, static_file

##################################################
@get('/app.js')
def _():
    return static_file('app.js', root='./js')
    
##################################################
@get('/navigation.js')
def _():
    return static_file('navigation.js', root='./js')

##################################################
@get('/signup.js')
def _():
    return static_file('signup.js', root='./js')

##################################################
@get('/login.js')
def _():
    return static_file('login.js', root='./js')

##################################################
@get('/home.js')
def _():
    return static_file('home.js', root='./js')

##################################################
@get('/tweets.js')
def _():
    return static_file('tweets.js', root='./js')

##################################################
@get('/follows.js')
def _():
    return static_file('follows.js', root='./js')

##################################################
@get('/admin.js')
def _():
    return static_file('admin.js', root='./js')