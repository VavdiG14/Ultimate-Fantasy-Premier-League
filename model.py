import sqlite3

#Pomožne funkcije s iskanjem SQL

baza = "Premier_Leauge.db"

# con = sqlite.connet(baza)
# cur = con.cursor()
# cur.execute('PRAGMA foreign keys=ON')



#TODO: uredi nekaj glede posodabljanja tabele Dogodki
#TODO: dodaj funkcije: rezulat, tockeEkipa,
def rezultat(krog1):
    '''Funkcija an podlagi vnešenih rezultata, priredi točke za osvojeno zmago, remi ali poraz'''
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Tekma WHERE krog = {0}".format(str(krog1)))
        a = cur.fetchall()
        for i in a :
            print(i)
            if i[-2] == i[-1]:
                rez1 = 1
                rez2 = 1
            else:
                if i[-1] > i[-2]:
                    rez2 = 3
                    rez1 = 0
                else:
                    rez2 = 0
                    rez1 = 3
            cur.execute("SELECT tocke FROM Lestvica WHERE ID_kluba = '{0}'".format(i[3]))
            zdajsne1 = cur.fetchall()
            cur.execute("SELECT tocke FROM Lestvica WHERE ID_kluba = '{0}'".format(i[4]))
            zdajsne2 = cur.fetchall()
            nove1 = int(zdajsne1[0][0]) + rez1
            cur.execute("UPDATE Lestvica SET tocke={0} WHERE ID_kluba = '{1}'".format(nove1, i[3]))
            nove2 = int(zdajsne2[0][0]) + rez2
            cur.execute("UPDATE Lestvica SET tocke ={0} WHERE ID_kluba = '{1}'".format(nove2,i[4]))
    return

def gk(tuple):
    (gol, asistenca, rumeni_karton, rdeci_karton, clean_sheet, branjene_11m, zgresene_11m, minute, avtogol, prejeti_goli)  = tuple
    prvi = sum((gol*10,asistenca*8, rumeni_karton*(-1), rdeci_karton*(-4),clean_sheet*(6)))
    drugi = sum((branjene_11m*6, zgresene_11m*(-3), avtogol* (-3)))
    if minute > 60:
        tretji = 2
    else:
        if minute != 0:
            tretji = 1
        else:
            tretji = 0
    if prejeti_goli >= 1:
        stiri = (prejeti_goli - 1 ) * (-1)
    else:
        stiri = 0
    return sum((prvi, drugi, tretji, stiri))
# GK: cleanSheet: 6, gol: 10, asistenca: 8, rumeni: -1, rdeči: -4, 60min: 2,avtogol:-2

def defender(tuple):
    (gol, asistenca, rumeni_karton, rdeci_karton, clean_sheet, branjene_11m, zgresene_11m, minute, avtogol, prejeti_goli)  = tuple
    prvi = (gol*6,asistenca*4, rumeni_karton*(-1), rdeci_karton*(-3),clean_sheet*4)
    drugi = (branjene_11m*10, zgresene_11m*(-3), avtogol* (-3))
    if minute > 60:
        tretji = 2
    else:
        if minute != 0:
            tretji = 1
        else:
            tretji = 0
    if prejeti_goli >= 1:
        stiri = (prejeti_goli - 1 ) * (-1)
    else:
        stiri = 0
    return sum((sum(prvi), sum(drugi), tretji, stiri))
#DEF: cleanSheet: 4, gol: 6, asistenca: 4, rumeni: -1, rdeči: -3, 60min: 2

def midfielder(tuple):
    (gol, asistenca, rumeni_karton, rdeci_karton, clean_sheet,
     branjene_11m, zgresene_11m, minute, avtogol,prejeti_goli) = tuple
    prvi = (gol *4, asistenca * 3, rumeni_karton * (-1), rdeci_karton * (-3), clean_sheet * 2)
    drugi = (branjene_11m * 10, zgresene_11m * (-3), avtogol * (-3))
    if minute > 60:
        tretji = 2
    else:
        if minute != 0:
            tretji = 1
        else:
            tretji = 0
    if prejeti_goli >= 1:
        stiri = (prejeti_goli - 1) * (-1)
    else:
        stiri = 0
    return sum((sum(prvi), sum(drugi), tretji, stiri))
#MID: cleanSheet: 2, gol:4, aistenca: 3, rumeni: -1,  rdeči: -3, 60min: 2


def fwd(tuple):
    (gol, asistenca, rumeni_karton, rdeci_karton, clean_sheet,
     branjene_11m, zgresene_11m, minute, avtogol, prejeti_goli) = tuple
    prvi = (gol * 3, asistenca * 4, rumeni_karton * (-1), rdeci_karton * (-3), clean_sheet *1)
    drugi = (branjene_11m * 10, zgresene_11m * (-3), avtogol * (-3))
    if minute > 60:
        tretji = 2
    else:
        if minute != 0:
            tretji = 1
        else:
            tretji = 0
    if prejeti_goli >= 1:
        stiri = (prejeti_goli - 1) * (-1)
    else:
        stiri = 0
    return sum((sum(prvi), sum(drugi), tretji, stiri))
#FWD: cleSheet: 0, gol:3, asistenca: 4, rumeni: -1, rdeči: -3, 60min: 2


def tockeTedna(krog1):
    '''Priredi točke glede na njegovo statisitko '''
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT Igralci.id_igralca, ime, pozicija, gol,asistenca, rumeni_karton, rdeci_karton,clean_sheet, branjene_11m,"
                    " zgresene_11m, minute, avtogol, prejeti_goli FROM Dogodki LEFT JOIN Igralci "
                    "ON  Dogodki.id_igralca = Igralci.id_igralca WHERE krog = {0}".format(str(krog1)))
        a = cur.fetchall()
        for igralec in a:
            id_igralca1 = igralec[0]
            ime, pozicija, = igralec[1],igralec[2]
            tocke = 0
            if pozicija == "GK":
                tocke = gk(igralec[3:])
            elif pozicija == "DEF":
                tocke  = defender(igralec[3:])
            elif pozicija == "MID":
                tocke = midfielder(igralec[3:])
            elif pozicija == "FWD":
                tocke = fwd(igralec[3:])
            cur.execute("INSERT INTO Tocke VALUES({0}, '{1}' ,{2})".format(id_igralca1, krog1, tocke))

    return

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
        cur.execute("INSERT INTO Uporabnik VALUES('{0}', '{1}', '{2}', '{3}')".format(username, password, email, team))
    return


###PRIJAVA

def preveriPrijavo(username,password):
    with sqlite3.connect(baza) as con:
        cur = con.cursor()
        cur.execute("SELECT uporabnisko_ime,geslo,ekipa FROM Uporabnik WHERE uporabnisko_ime = '{0}'".format(username))
        a = cur.fetchall()
        print(a)
        if a != []:
            if a[0][1] == password:
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
        if igralec[0][2] == 'GK':
            gk.append(igralec[0])
        elif igralec[0][2] == 'DEF':
            def1.append(igralec[0])
        elif igralec[0][2] == 'MID':
            mid.append(igralec[0])
        else:
            fwd.append(igralec[0])
    return (gk,def1,mid,fwd)