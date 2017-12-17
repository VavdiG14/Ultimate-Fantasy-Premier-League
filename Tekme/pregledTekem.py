import requests
#import loger
import datetime
from bs4 import BeautifulSoup
import os

def tekma(stevilkaTekme):
    data = requests.get("https://www.premierleague.com/match/{0}".format(stevilkaTekme)) #Išcemo po spletni strani
    data1 = str(data.content, 'utf-8')
    soup = BeautifulSoup(data1,"lxml")
    igralci = soup.findAll('div',{'class':'name'})
    krogSoup = soup.find('div',{'class':'long'})
    vSeznam = krogSoup.text.split(" ")
    krog = vSeznam[1].strip()
    titleSoup = soup.find("meta",  property="og:title")
    nas = titleSoup['content'].split(',')[0]
    naslov = nas.replace(" ", "_")
    naslov1 = krog +'_'+naslov
    stevec  = 0
    with open('{0}.txt'.format(naslov1), 'w') as f:
        for i in igralci:
            if stevec == 18:
                print('-----------------',file=f)
            print(i.text.strip(),file=f)
            stevec += 1
        print('------DOMACI ----------',file=f)
        golD = soup.findAll('div', {'class':"home"})
        for st, j in enumerate(golD[:-1]):
            if st == 0:
                print('-------GOLI---------',file=f)
            if st == 2:
                print('-------ASISTENCE----------',file=f)
            if st == 3:
                print('-------POTEK TEKME--------',file=f)
            print(j.text.strip(),file=f)
        print('----GOSTJE ---------',file=f)
        golG = soup.findAll('div', {'class':'away'})
        for st, h in enumerate(golG[:-1]):
            if st == 0:
                print('-------GOLI---------',file=f)
            if st == 2:
                print('-------ASISTENCE----------',file=f)
            if st == 3:
                print('-------POTEK TEKME--------',file=f)
            print(h.text.strip(),file=f)
    return (krog, (naslov1+'.txt'))

def minute(vhodna_datoteka):
    with open(vhodna_datoteka,'r') as g:
        shrani = 0
        stej = 0
        prejšni = False
        with open ('{0}-minute.txt'.format(vhodna_datoteka), 'w') as n:
            for s,vrstica in enumerate(g):
                vrstica = vrstica.strip()
                if stej < 11:
                    minute = 90
                else:
                    minute = 0
                if len(vrstica) == 0:
                    continue

                if not vrstica[0].isnumeric() and prejšni== True:
                    print(shrani+';'+str(minute), file=n)
                    stej += 1
                    prejšni = False
                if vrstica == '-----------------':
                    stej = 0
                    print(vrstica, file=n)
                    continue
                if not vrstica[0].isnumeric():
                    shrani = vrstica
                    prejšni = True
                if vrstica[0].isnumeric():
                    print(str(shrani)+';'+vrstica, file=n)
                    prejšni = False
                    stej += 1

                elif vrstica == '------DOMACI ----------':
                    break
    return '{0}-minute.txt'.format(vhodna_datoteka)

def goli(vhodna_datoteka):
    dvojka = 0
    goli= False
    asistence = False
    with open(vhodna_datoteka,'r') as g:
        with open ('{0}-goli.txt'.format(vhodna_datoteka), 'w') as n:        
            for vrstica in g:
                vrstica = vrstica.strip()
                if vrstica == '-------GOLI---------':
                    goli = True
                    print('-------GOLI---------',file=n)
                    dvojka = 0
                elif vrstica == '-------ASISTENCE----------':
                    asistence= True
                    #print('-------ASISTENCE----------',file=n)
                    goli = False
                    dvojka = 0
                elif vrstica == '-------POTEK TEKME--------':
                    asistence = False
                if len(vrstica) == 0:
                    continue
                elif 'Goal' == vrstica:
                    continue
                if goli and dvojka > 1:
                    print(vrstica, file = n)
                if  vrstica == 'Own Goal':
                    continue
                dvojka += 1
                if asistence:
                    print(vrstica, file = n)
    return '{0}-goli.txt'.format(vhodna_datoteka)

                    
def kartoni(vhodna_datoteka):
    with open(vhodna_datoteka,'r') as g:
        zacni = False
        with open('{0}-kartoni.txt'.format(vhodna_datoteka), 'w') as p:
            o = 0
            for vrstica in g:
                vrstica = vrstica.strip()
                #print(vrstica[0:11])
                if vrstica[0:11] == 'Yellow Card':
                    zacni = True
                    print('--RUMENI KARTONI---', file=p)
                    o = 0
                o += 1
                if o == 21 and zacni:
                    print(vrstica, file=p)

    return '{0}-kartoni.txt'.format(vhodna_datoteka)
