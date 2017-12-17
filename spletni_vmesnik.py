import modeli
from bottle import *

# @get('/')
# def glavniMenu():
#     return template('glavni.html')
#
# @get('/static/<filename:path>')
# def static(filename):
#     return static_file(filename, root='static')
#
# @get('/oseba/<emso>')
#
# @get('/isci')
#
# @post('/dodaj')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True)