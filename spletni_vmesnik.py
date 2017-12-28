import model
from bottle import *

@get('/')
def glavniMenu():
      return template('index.html')

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/registriraj')
def registriraj():
    return template('registriraj.html')
#
@get('/prijava')
def prijava():
    return template('prijava.html')
#
# @post('/dodaj')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True)