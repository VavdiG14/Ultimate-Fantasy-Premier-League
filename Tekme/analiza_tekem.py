from pregledTekem import*
from collections import Counter

class Igralec():

    def __init__(self, ime, minute=0, goli=0, asistence=0, rumeniKartoni=0, rdeciKartoni=0):
        self.ime = ime
        self.m = minute
        self.g = goli
        self.a = asistence
        self.rumeniK = rumeniKartoni
        self.rdeciK =rdeciKartoni

    def __repr__(self):
        return 'Igralec(' + self.ime + ", " + str(self.m)+ ", " + str(self.g)+ ", " + str(self.a)+ ", " + str(self.rumeniK)+ ", " + str(self.rdeciK) +')'

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
    if  '(og)' in string:
        stej = -1* stej
    return (ime, stej)


def izberiTekmo(stevilkaTekme = '22367'):
    '''String stevilke, da dobimo določeno tekmo'''
    krog, vhodna = tekma(stevilkaTekme)
    izhodna_goli = goli(vhodna)
    with open(izhodna_goli, 'r') as g:
        asistenca = []
        rdeciKarton = []
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
                if vrsta == 'Red Card':
                    rdeciKarton.append(gol[-1])
                    gol = gol[:-1]
                else:
                    gol.append(vrsta)
            elif asis:
                asistenca.append(vrsta)
    return (vhodna, gol, asistenca, rdeciKarton)
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
        goli_klubD += int(steviloGolovAsistenc(j)[1])
        strelciD[steviloGolovAsistenc(j)[0]] = steviloGolovAsistenc(j)[1]
    for l in goliG:
        goli_klubG += steviloGolovAsistenc(l)[1]
        strelciG[steviloGolovAsistenc(l)[0]] = steviloGolovAsistenc(l)[1]
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
    e = 0
    with open(izhodna_minute, 'r') as f:
        for vrstica in f:
            e += 1
            vrstica = vrstica.strip()
            seznam = vrstica.split(';')
            ime = seznam[0]
            if seznam == ['-----------------']:
                e = 0
                continue
            if e > 11:
                if seznam[1] == '0':
                    minuta = 0
                else:
                    se = seznam[1].split("'")
                    minuta = 90 - int(se[0])
            else:
                minuta = seznam[1][0:2]
            trenutniIgralec = Igralec(ime)
            if trenutniIgralec.ime in list(strelci.keys()):
                trenutniIgralec.g = strelci[trenutniIgralec.ime]
            if trenutniIgralec.ime in list(podajalci.keys()):
                trenutniIgralec.a = podajalci[trenutniIgralec.ime]
            if trenutniIgralec.ime in list(rumeni.keys()):
                trenutniIgralec.rumeniK = rumeni[trenutniIgralec.ime]
            if trenutniIgralec.ime in rdeciKarton:
                trenutniIgralec.rdeciK = 1
            trenutniIgralec.m = minuta
            igralci.append(trenutniIgralec)
    return igralci

for i in range(22342, 22351):
    vhodna, gol, asistenca, rdeci = izberiTekmo(str(i))
    strelci, podajalci, rezultat = vSlovar(gol, asistenca)
    #rumeni = vSlovarKartoni(vhodna)
    #igralci = vRazredIgralec(vhodna, rumeni, strelci, podajalci, rdeci)

    #print(strelci, podajalci)
    print(rezultat)
#print(igralci)