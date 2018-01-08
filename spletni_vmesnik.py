from model import *
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
##    baza = "Premier_Leauge.db"
##    con = sqlite.connect(baza)
##    cur = con.cursor()
##    tabela=cur.execute("SELECT * FROM Lestvica ORDER BY tocke DESC")
    return dict(title="UFPL", content="Pozdravljeni na Ultimate Fantasy Premier League!")




@get('/registracija')
def registriraj():
    return template('registracija.html', opozorilo = " ")
#
@get('/prijava')
def prijava():
    return template('prijava.html', opozorilo = " ")

@get('/izberi_ekipo')
def izberiEkipo():

    return template('izberi_ekipo.html')


@get('/contact')
def onaju():
    return template('oprojektu.html')


@post('/register')
def registriraj():
    username = request.forms.get('username')
    email =  request.forms.get('email')
    team = request.forms.get('team_name')
    password =  request.forms.get('password')
    confirm = request.forms.get('password2')
    if "" in [username, email, team, password, confirm]:
        return template('registracija.html', opozorilo='Izpolni vsa okna za prijavo')
    if password != confirm:
        return template('registracija.html', opozorilo = 'Gesli se ne ujemata')
    if preveriPristnost(username, email, team, password)[0]:
        shraniUporabnika(username, email, team, password)
        return redirect('izberi_ekipo')
    else:
        return template('registracija.html', opozorilo = preveriPristnost(username, email, team, password)[1])

    #TODO: Sheširaj geslo


@post('/signup')
def prijava():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if preveriPrijavo(username,password)[0]:
        return redirect('/prva_stran/{0}'.format(username))
    else:
        return template('prijava.html', opozorilo = preveriPrijavo(username, password)[1])

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
