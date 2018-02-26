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
        cur.execute("INSERT INTO Uporabnik VALUES('{0}', '{1}', '{2}', '{3}','None', 0,0, 'None',1)".format(username, hashing(password), email, team))
    return


###PRIJAVA

def preveriPrijavo(username,password):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT uporabnisko_ime,geslo,ekipa FROM Uporabnik WHERE uporabnisko_ime = '{0}'".format(username))
        a = cur.fetchall()
        print(a)
        if a != []:
            if a[0][1] == hashing(password):
                if a[0][2] == 'None':
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

def shraniEkipo(string, uporabnik):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("UPDATE Uporabnik SET ekipa = '{0}' WHERE uporabnisko_ime ='{1}'".format(string, uporabnik))
    return

def poisciUporabnika(username):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT ime_ekipe,ekipa, tocke_skupaj, tocke_krog, tocke_krog_nazaj, krog FROM Uporabnik WHERE uporabnisko_ime = '{0}'".format(username))
        return cur.fetchall()

def poisciIgralca(id):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT ime, klub, pozicija FROM Igralci WHERE id_igralca = {0}".format(id))
        return cur.fetchall()

def postaviIgralce(string):
    gk = []
    def1 = []
    mid = []
    fwd = []
    sez = string[1:-1]
    sez1 = list(map(int, sez.split(",")))
    for i in sez1:
        igralec = poisciIgralca(i)
        print(igralec)
        if igralec[0][2] == 'GK':
            gk.append((igralec[0][0], igralec[0][1], igralec[0][2], "/assets/img/dres_{0}.png".format(igralec[0][1])))
        elif igralec[0][2] == 'DEF':
            def1.append((igralec[0][0], igralec[0][1], igralec[0][2], "/assets/img/dres_{0}.png".format(igralec[0][1])))
        elif igralec[0][2] == 'MID':
            mid.append((igralec[0][0], igralec[0][1], igralec[0][2], "/assets/img/dres_{0}.png".format(igralec[0][1])))
        else:
            fwd.append((igralec[0][0], igralec[0][1], igralec[0][2], "/assets/img/dres_{0}.png".format(igralec[0][1])))
    return (gk,def1,mid,fwd)

def nastaviTocke(krog,izbranih):
    tocke1 = []
    for i in izbranih:
        if i == 0:
            tocke1.append(0)
            continue
        with sqlite3.connect(baza) as con:
            cur = con.cursor()
            cur.execute("SELECT tocke FROM Tocke WHERE id_igralca = '{0}' AND krog = '{1}'".format(i,krog))
            a = cur.fetchall()
            if a == []:
                tocke1.append(0)
            else:
                tocke1.append(a[0][0])
    vsota = sum(tocke1)
    return (tocke1,vsota)

def posodobiBazo(seznamTock, vsota,krog,username):
    b = ','.join(str(e) for e in seznamTock)
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("UPDATE Uporabnik SET tocke_krog_nazaj = '{3}', tocke_krog = {0}, krog = '{1}', "
                    "tocke_skupaj = tocke_skupaj + {0} WHERE uporabnisko_ime = '{2}'".format(vsota, str(int(krog)+1), username,b ))
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