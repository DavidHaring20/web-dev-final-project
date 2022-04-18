from bottle import get, static_file

##################################################
@get('/app.css')
def _():
    return static_file('app.css', root='./stylesheets')

##################################################
@get('/landing-page.css')
def _():
    return static_file('landing-page.css', root='./stylesheets')