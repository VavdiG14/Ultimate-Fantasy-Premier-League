from pregledTekem import*
from collections import Counter

class Igralec():

    def __init__(self, ime, minute=0, goli=0, asistence=0, rumeniKartoni=0, rdeciKartoni=0,og = 0):
        self.ime = ime
        self.m = minute
        self.g = goli
        self.a = asistence
        self.rumeniK = rumeniKartoni
        self.rdeciK =rdeciKartoni
        self.og = og

    def __repr__(self):
        return 'Igralec(' + self.ime + ", " + str(self.m)+ ", " + str(self.g)+ ", " + str(self.a)+ ", " +\
               str(self.rumeniK)+ ", " + str(self.rdeciK) + ", " + str(self.og)+')'



def steviloGolovAsistenc(string):
    '''Niz oblike: "Jesse Lingard 11', 63'", prebere igralca in določi številko golov. Vrne ime igralca in število golov.
    Posebnost:  "Lewis Dunk 89' (og)"'''

    sez = string.split(' ')
    if sez[1][0].isnumeric():
        ime = sez[0]
    elif sez[2][0].isnumeric():
        ime = sez[0] +' '+sez[1]
    else:
        ime = sez[0] +' '+sez[1] + ' ' + sez[2]
    stej = string.count("'")
    stejog = string.count("(og)")
    return (ime, stej-stejog, stejog )

def minutaRdeciKarton(string):
    se = string.split(" ")
    min = se[-1][:-1]
    ime = ""
    for i in se[:-1]:
        ime += i
        ime += " "
    return ime[:-1], int(min)



def izberiTekmo(stevilkaTekme = '22367'):
    '''String stevilke, da dobimo določeno tekmo'''
    krog, vhodna = tekma(stevilkaTekme)
    izhodna_goli = goli(vhodna)
    with open(izhodna_goli, 'r') as g:
        asistenca = []
        rdeciKarton = dict()
        gol = []
        goal = True
        asis = False
        for vrsta in g:
            vrsta = vrsta.strip()
            if vrsta == '-------GOLI---------':
                goal = True
                asis = False
                continue
            elif vrsta == '-------ASISTENCE----------':
                goal = False
                asis = True
                continue
            if goal:

                if vrsta == 'Own Goal':
                    continue
                elif vrsta == 'label.penalty.scored':
                    continue
                if vrsta == 'Red Card' or vrsta == 'Second Yellow Card (Red Card)':
                    ime, min = minutaRdeciKarton(gol[-1])
                    rdeciKarton[ime] = min
                    gol = gol[:-1]
                else:
                    gol.append(vrsta)
            elif asis:
                asistenca.append(vrsta)
    return (krog, vhodna, gol, asistenca, rdeciKarton)
    #print(gol,asistenca,rdeciKarton)



def vSlovar(gol,asistenca):
    '''Iz seznama strelcev in asistentov naredi slovar po principu: ime: število golov/asistenc
    Naredi tudi tuple rezultata:'''
    podajalci = dict()
    rezultat = dict()
    strelciD =dict()
    strelciG = dict()
    goli_klubD = 0
    goli_klubG = 0
    inde = []
    for i in gol:
        if len(i) ==3:
            inde.append(gol.index(i))
    goliD = gol[inde[0]+1:inde[1]]
    goliG = gol[inde[1]+1:]
    for j in goliD:
        trojka = steviloGolovAsistenc(j)
        goli_klubD += int(trojka[1])
        goli_klubD += int(trojka[2])
        strelciD[trojka[0]] = (trojka[1],trojka[2])
    for l in goliG:
        trojka1 = steviloGolovAsistenc(l)
        goli_klubG += int(trojka1[1])
        goli_klubG += int(trojka1[2])
        if trojka1[0] in list(strelciD.keys()):
            t = strelciD[trojka1[0]]
            r = (t[0]+trojka1[1] ,t[1] + trojka1[2])
            strelciD[trojka1[0]] = r
        else:
            strelciG[trojka1[0]] = (trojka1[1],trojka1[2])
    for k in asistenca:
        podajalci[steviloGolovAsistenc(k)[0]] = steviloGolovAsistenc(k)[1]
    strelci = {**strelciD, **strelciG}
    rezultat[gol[inde[0]]] = goli_klubD
    rezultat[gol[inde[1]]] = goli_klubG
    return (strelci, podajalci, rezultat)


def vSlovarKartoni(vhodna):
    '''Iz datoteke prebere igralce, ki so dobili rumene kartone in naredi slovar.'''
    izhodna_kartoni = kartoni(vhodna)
    with open(izhodna_kartoni, 'r') as l:
        i = 0
        rumeniKartoni = []
        for line in l:
            line = line.strip()
            if i%2 != 0:
                pika = line.index(" ")
                rumeniKartoni.append(line[pika+1:])
            i+= 1

    rumeni = Counter(rumeniKartoni)
    return rumeni


def vRazredIgralec(vhodna_datoteka, rumeni,strelci,podajalci,rdeciKarton):
    izhodna_minute = minute(vhodna_datoteka)
    igralci = []
    imena = set()
    e = 0
    with open(izhodna_minute, 'r') as f:
        for vrstica in f:
            e += 1
            vrstica = vrstica.strip()
            seznam = vrstica.split(';')
            ime = seznam[0]
            if "'" in ime:
                ime = ime.replace("'", '"')
            if seznam == ['-----------------']:
                e = 0
                continue
            if e > 11:
                if seznam[1] == '0':
                    minuta = 0
                else:
                    se = seznam[1].split("'")
                    minuta = abs(90 - eval(se[0]))
            else:
                if "'" in seznam[1]:
                    p = seznam[1].index("'")
                else:
                    p = 2
                minuta = seznam[1][0:p]

            trenutniIgralec = Igralec(ime)
            if trenutniIgralec.ime in list(strelci.keys()):
                trenutniIgralec.g = strelci[trenutniIgralec.ime][0]
                trenutniIgralec.og = strelci[trenutniIgralec.ime][1]
            if trenutniIgralec.ime in list(podajalci.keys()):
                trenutniIgralec.a = podajalci[trenutniIgralec.ime]
            if trenutniIgralec.ime in list(rumeni.keys()):
                trenutniIgralec.rumeniK = rumeni[trenutniIgralec.ime]
            if trenutniIgralec.ime in list(rdeciKarton.keys()):
                trenutniIgralec.rdeciK = 1
                trenutniIgralec.m = rdeciKarton[ime]
            else:
                trenutniIgralec.m = minuta
            if ime not in imena:
                igralci.append(trenutniIgralec)
                imena.add(ime)
    return igralci


import sqlite3


baza = "Ultimate-Fantasy-Premier-Leauge/Premier_Leauge.db"

for i in range(22351, 22352):
    print(i)
    krog, vhodna, gol, asistenca, rdeci = izberiTekmo(str(i))
    strelci, podajalci, rezultat = vSlovar(gol, asistenca)
    rumeni = vSlovarKartoni(vhodna)
    igralci = vRazredIgralec(vhodna, rumeni, strelci, podajalci, rdeci)
    id_dom = list(rezultat.keys())[0]
    id_gost = list(rezultat.keys())[1]
    goli_d = rezultat[id_dom]
    goli_g = rezultat[id_gost]
    print(rezultat)
    with sqlite3.connect(baza) as con:
        cur = con.cursor()  # "odzivnik" za pregledovanje poizvedbe
        cur.execute("INSERT INTO Tekma VALUES ({0}, 0, {1}, '{2}', '{3}', {4}, {5})".format(i, krog, id_dom, id_gost, goli_d, goli_g))
        for v,k in enumerate(igralci):
            cleanSheet = None
            prejeti = 0
            if v > 18:  #gostje
                if goli_d == 0:
                    cleanSheet = True
                else:
                    cleanSheet = False
                    prejeti = goli_d
            else:
                if goli_g == 0:
                    cleanSheet = True
                else:
                    cleanSheet = False
                    prejeti = goli_g
            cur.execute("SELECT id_igralca FROM Igralci WHERE '{0}' == ime".format(k.ime))
            id_i = cur.fetchone()
            if id_i is None:
                continue
            print(id_i[0])
            print(k)
            #cur.execute("INSERT INTO  Dogodki VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},0,0,{9},{10})".format(i, id_i[0], krog, k.g, k.a, k.rumeniK, k.rdeciK,int(cleanSheet), k.m, k.og, prejeti))