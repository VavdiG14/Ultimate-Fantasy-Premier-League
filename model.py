import sqlite3 as sq

#Pomožne funkcije s iskanjem SQL

baza = "Premier_Leauge.db"
con = sq.connect(baza)
cur = con.cursor()


#TODO: uredi tabelo TEKME, spremeni kratice tekem in dodaj vse še neodigrane
#TODO: uredi nekaj glede posodabljanja tabele Dogodki
#TODO: dodaj funkcije: rezulat, tockeEkipa,
def rezulat():
    '''Funkcija an podlagi vnešenih dogodki, izračuna  rezultat vseh tekem tistega kroga.
        Funkcija vrača '''
    for idEkipe in IDekip:
        cur.execute(
            """
            
            """
        )
    return 0

