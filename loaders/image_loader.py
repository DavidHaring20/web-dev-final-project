from bottle import get, static_file

##################################################
@get('/images/<image_name>')
def _(image_name):
    return static_file(image_name, root='./images')

##################################################
@get('/illustrations/<illustration_name>')
def _(illustration_name):
    return static_file(illustration_name, root='./illustrations')