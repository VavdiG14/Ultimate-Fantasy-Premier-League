import sqlite3
import hashlib

#Pomožne funkcije s iskanjem SQL

baza = "Premier_Leauge.db"

# con = sqlite.connet(baza)
# cur = con.cursor()
# cur.execute('PRAGMA foreign keys=ON')

def hashing(password):
    b = str.encode(password)
    hash_object = hashlib.sha256(b)
    hex_dig = hash_object.hexdigest()
    return hex_dig


#TODO: uredi nekaj glede posodabljanja tabele Dogodki
#TODO: dodaj funkcije: rezulat, tockeEkipa,

###REGISTRACIJA

def preveriPristnost(username, email, team, password):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT uporabnisko_ime, geslo, email, ime_ekipe FROM Uporabnik WHERE uporabnisko_ime = '{0}'".format(username))
        a = cur.fetchall()
        if a == []:
            return (True, "")
        else:
            return (False, 'Uporabniško ime že zasedeno')

def shraniUporabnika(username, email, team, password):

    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Uporabnik VALUES(NULL ,'{0}', '{1}', '{2}', '{3}','None', 0,0, 'None',1)".format(username, hashing(password), email, team))
    return


###PRIJAVA

def preveriPrijavo(username,password):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_igralca FROM Ekipa WHERE id_uporabnika = (SELECT id_uporabnika FROM Uporabnik WHERE uporabnisko_ime = '{0}')".format(username))
        b = cur.fetchall()
        cur.execute("SELECT uporabnisko_ime,geslo FROM Uporabnik WHERE uporabnisko_ime = '{0}'".format(username))
        a = cur.fetchall()
        print(a)
        if a != []:
            if a[0][1] == hashing(password):
                if b == []:
                    return (True, None)
                else:
                    return (True, "")
            else:
                return (False, "Geslo se ne ujema. Poskusi ponovno.")
        else:
            return (False, 'Uporabnik ni registriran')

def pokaziIgralce():
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_igralca,ime, pozicija, klub, cena FROM Igralci")
        return cur.fetchall()

def lestvica():
    with sqlite3.connect(baza) as con:
        cur=con.cursor()
        cur.execute("SELECT ime,tocke FROM Lestvica ORDER BY tocke DESC")
        return cur.fetchall()

def shraniEkipo(seznam, username):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_uporabnika FROM Uporabnik WHERE uporabnisko_ime ='{0}'".format(username))
        id_uporabnika = int(cur.fetchall()[0][0])
        print(id_uporabnika, seznam)
        for i in seznam:
            cur.execute("INSERT INTO Ekipa VALUES({0}, {1})".format(id_uporabnika, int(i)))
    return

def poisciUporabnika(username):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT ime_ekipe, tocke_skupaj, tocke_krog, krog FROM Uporabnik WHERE uporabnisko_ime = '{0}'".format(username))
        return cur.fetchall()

def poisciIgralca(id):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT ime, klub, pozicija FROM Igralci WHERE id_igralca = {0}".format(id))
        return cur.fetchall()

def poisiciEkipo(username):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_igralca FROM Ekipa WHERE id_uporabnika = "
                    "(SELECT id_uporabnika FROM Uporabnik WHERE uporabnisko_ime ='{0}')".format(username))
    return cur.fetchall()

def postaviIgralce(username, krog):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_uporabnika, krog FROM Uporabnik WHERE uporabnisko_ime ='{0}'".format(username))
        user = cur.fetchall()[0][0]
        prejsni_krog = krog - 1
        cur.execute("SELECT Odigran_krog.id_igralca, Odigran_krog.tocke, Igralci.ime, Igralci.klub, Igralci.pozicija FROM Odigran_krog JOIN Igralci ON Odigran_krog.id_igralca=Igralci.id_igralca WHERE Odigran_krog.id_uporabnika = {0} AND Odigran_krog.krog = {1}".format(user, prejsni_krog))
        seznam = cur.fetchall()
        print(seznam)
    seznamIgralcev = []
    gk = []
    def1 = []
    mid = []
    fwd = []
    for i in seznam:
        seznamIgralcev.append(i[0])
        if i[4] == 'GK':
            gk.append((i[2], i[3], i[1], "/assets/img/dres_{0}.png".format(i[3])))
        elif i[4] == 'DEF':
            def1.append((i[1], i[2], i[3], "/assets/img/dres_{0}.png".format(i[3])))
        elif i[4] == 'MID':
            mid.append((i[1], i[2], i[3], "/assets/img/dres_{0}.png".format(i[3])))
        else:
            fwd.append((i[1], i[2], i[3], "/assets/img/dres_{0}.png".format(i[3])))

    return (gk,def1,mid,fwd,seznamIgralcev)


def nastaviTocke(krog,rezerve, mojih15, username):
    sez = []
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT Tocke.id_igralca, Tocke.tocke FROM Ekipa INNER JOIN Tocke ON (Tocke.id_igralca = Ekipa.id_igralca) "
                    "WHERE krog = '{0}' AND id_uporabnika = (SELECT id_uporabnika FROM Uporabnik WHERE uporabnisko_ime ='{1}')".format(krog,username))
        seznamTock = cur.fetchall()
    print(seznamTock)
    print("SPDaj")
    print(mojih15)
    vsota = 0
    sezn = [s[0] for s in seznamTock]
    for id_igralca1 in mojih15:
        id_igralca = id_igralca1[0]
        if int(id_igralca) in rezerve:
            sez.append((id_igralca, 0))
        elif int(id_igralca) in sezn:
            i = sezn.index(id_igralca)
            sez.append((id_igralca,seznamTock[i][1]))
            vsota += int(seznamTock[i][1])
        else:
            sez.append((id_igralca,0))
    print(sez)
    return (sez, vsota)

def posodobiBazo1(seznamTock,krog, username ):
    """Posodobi tabelo Odigran krog in nastavi krog,id_igralca, id_uporabnika, tocke"""
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_uporabnika FROM Uporabnik WHERE uporabnisko_ime ='{0}'".format(username))
        user = cur.fetchall()[0][0]
    for id_igralca, tocke in seznamTock:
        with sqlite3.connect(baza) as con:
            cur = con.cursor()
            cur.execute(" INSERT INTO Odigran_krog VALUES({1},{2}"
                        ",'{0}', {3})".format(krog, id_igralca, user, tocke))
    return

def poisciTocke(username,krog):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT id_uporabnika FROM Uporabnik WHERE uporabnisko_ime ='{0}'".format(username))
        user = cur.fetchall()[0][0]
        cur.execute("SELECT id_igralca, tocke FROM Odigran_krog WHERE krog = {0} AND id_uporabnika = {1}".format(krog,user))
        return cur.fetchall()



def posodobiBazo(vsota,krog,username):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("UPDATE Uporabnik SET tocke_krog = {0}, krog = '{1}', "
                    "tocke_skupaj = tocke_skupaj + {0} WHERE uporabnisko_ime = '{2}'".format(vsota, str(int(krog)+1), username))
    return

def pregledKroga(krog):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT domaci,goli_domaci, goli_gostje, gostje, krog FROM Tekma WHERE krog = '{0}'".format(str(int(krog)-1)))
    return cur.fetchall()

def napovedKroga(krog):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT domaci,gostje, krog FROM Tekma WHERE krog = '{0}'".format(krog))
    return cur.fetchall()

def najkoristnejsiIgralci():
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT SUM(tocke),ime FROM Tocke INNER JOIN Igralci ON (Igralci.id_igralca = Tocke.id_igralca) "
                    "GROUP BY Tocke.id_igralca ORDER BY SUM(tocke) DESC LIMIT 10")
        return cur.fetchall()


def lestivcaUporabnikov():
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT uporabnisko_ime, tocke_skupaj, krog FROM Uporabnik LIMIT 10")
        return cur.fetchall()