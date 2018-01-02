import model
from bottle import *

import os
from bottle import route, run, static_file, template, view

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./js')

@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./img')

@route('/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./css')

@route("/")
@view("index")
def glavniMenu():
    return dict(title="Hello", content="Hello from Python!")




@get('/registracija')
def registriraj():
    return template('registracija.html')
#
@get('/prijava')
def prijava():
    return template('prijava.html')


@get('/contact')
def onaju():
    return template('oprojektu.html')



# @post('/dodaj')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True)