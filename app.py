#!/usr/bin/env python

import os
from bottle import route, run, static_file, template, view,get,post,request,redirect,response
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
def glavniMenu():
    return template('index.html', najkoristnejsiIgralci = najkoristnejsiIgralci(),
                    lestvica = lestvica())


@route('/izberiEkipo')
def izberiEkipo():
    return template('izberiEkipo.html', rezultat=pokaziIgralce())


@get('/registracija')
def registriraj():
    return template('registracija.html', opozorilo = None)


@get('/prijava')
def prijava():
    return template('prijava.html', opozorilo = None)

@post('/signup')
def prijava():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if preveriPrijavo(username,password)[0]:
        response.set_cookie("racun", username, secret='some-secret-key1')
        if preveriPrijavo(username,password)[1] is None:    #ko se prijaviš pogleda ali je stolpec ekipa prazen, #  če je te vrže na izberiIgralce, drugače na mojteam
            return redirect('izberiEkipo')
        else:
            return redirect('myTeam')
    else:
        return template('prijava.html', opozorilo = preveriPrijavo(username, password)[1])



@post('/ekipa')
def sestaviEkipo():
    username = request.get_cookie("racun", secret='some-secret-key1')
    igralci = request.forms.getall('gk')
    print(igralci, username)
    shraniEkipo(list(map(int,igralci)), username)
    return redirect('/myTeam')

def spremeni(tupl):
    izid = str(tupl[1])+ " : " + str(tupl[2])
    return (tupl[-1],tupl[0], izid, tupl[3])

@get('/myTeam')
def myTeam():
    username = request.get_cookie("racun", secret='some-secret-key1')
    print(username)
    if username:
        ime_ekipe, ekipa, tocke_skupaj, tocke_krog, tocke_krog_nazaj, krog = poisciUporabnika(username)[0]
        print(tocke_krog_nazaj)
        if tocke_krog_nazaj != 'None':
            seznamTock = list(map(int,tocke_krog_nazaj.split(',')))
        else:
            seznamTock = None
        golmani,obramba,zvezna,napadalci = postaviIgralce(ekipa)
        if int(krog) <= 1:
            tekme = None
        else:
            tekme = [spremeni(i) for i in pregledKroga(krog)]
        napoved = napovedKroga(krog)
        return template('myTeam.html', ime_ekipe=ime_ekipe, golmani=golmani,
                    obramba=obramba,
                    sredina=zvezna,
                    napad=napadalci,
                    seznamIgralcev = ekipa,
                    seznamTock=seznamTock,
                    tocke_krog=tocke_krog,
                    tocke_skupaj=tocke_skupaj,
                    krog=krog,
                    pregledKroga = tekme,
                    napovedKroga = napoved)
    else:
        return redirect('prijava')

@post('/krog')
def izracunajKrog():
    username = request.get_cookie("racun", secret='some-secret-key1')
    igralci = request.forms.getall('mojih11')
    izbrani = list(map(int,igralci))
    print(igralci)
    if username:
        uporab = poisciUporabnika(username)[0]
        krog = uporab[-1]
        seznamTock,vsota = nastaviTocke(krog,izbrani)
        posodobiBazo(seznamTock, vsota,krog,username)
        return redirect('/myTeam')

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
        response.set_cookie("racun", username, secret='some-secret-key1')
        return redirect('izberiEkipo')
    else:
        return template('registracija.html', opozorilo = preveriPristnost(username, email, team, password)[1])

    #TODO: Sheširaj geslo



@get('/prva_stran')
def prvaStran():
    rezultat=lestvica()
    return template('prva_stran.html', rezultat=rezultat)


# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
