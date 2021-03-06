from bottle import get, static_file

##################################################
@get('/app.css')
def _():
    return static_file('app.css', root='./stylesheets')

##################################################
@get('/landing-page.css')
def _():
    return static_file('landing-page.css', root='./stylesheets')

##################################################
@get('/signup-modal.css')
def _():
    return static_file('signup-modal.css', root='./stylesheets')

##################################################
@get('/login-modal.css')
def _():
    return static_file('login-modal.css', root='./stylesheets')

##################################################
@get('/home.css')
def _():
    return static_file('home.css', root='./stylesheets')

##################################################
@get('/admin.css')
def _():
    return static_file('admin.css', root='./stylesheets')