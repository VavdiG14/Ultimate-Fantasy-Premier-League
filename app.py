#!/usr/bin/env python

import os
from bottle import route, run, static_file, template, view,get,post,request,redirect
from model import *

# Static Routes
@get("/assets/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./assets/css")

@get("/assets/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="./assets/fonts")

@get("/assets/img/<filepath:re:.*\.(jpg|png|gif|ico|svg|jpeg|JPG)>")
def img(filepath):
    return static_file(filepath, root="./assets/img")

@get("/assets/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./assets/js")


@route("/")
@view("index")
def glavniMenu():
    return


@get('/registracija')
def registriraj():
    return template('registracija.html', opozorilo = None)


@get('/prijava')
def prijava():
    return template('prijava.html', opozorilo = None)

@get('/ekipa')
def izberiEkipo():
    return template('ekipa.html', rezultat= pokaziIgralce())

@get('/team')
def mojaEkipa():
    return template('team.html',ime_ekipe = "KANDIX", golmani = [("David De Gea", "MAN UTD"),("Salah", "MAN UTD")],
                    obramba = [("Salah", "MAN UTD"),("Salah", "MAN UTD"), ("Phil Jones", "MAN UTD"), ("Davies", "TOT"),("Gomez", "TOT")],
                    sredina=[("N'Kate", "LIV"), ("Salah", "MAN UTD"), ("Valencia", "TOT"), ("Hazard", "TOT"),("Blaz Poljanec", "LIV")],
                    napad=[("Sergio Aguero", "LIV"), ("Lukaku", "MAN UTD"),("Hazard", "TOT")]
                    )


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
        return redirect('ekipa')
    else:
        return template('registracija.html', opozorilo = preveriPristnost(username, email, team, password)[1])

    #TODO: Sheširaj geslo


@post('/signup')
def prijava1():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if preveriPrijavo(username,password)[0]:
        return redirect('team')
    else:
        return template('prijava.html', opozorilo = preveriPrijavo(username, password)[1])

@get('/prva_stran')
def prvaStran():
    rezultat=lestvica()
    return template('prva_stran.html', rezultat=rezultat)

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
