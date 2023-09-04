import sqlite3
import csv

def napolni_dirkaci():
    '''Napolni tabelo dirkaci'''
    with open("archive/drivers.csv", "r", encoding = 'utf-8') as dirkaci:
        csv_reader = csv.reader(dirkaci, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        for vrstica in csv_reader:
            tupl = tuple([vrstica[0]] + vrstica[4:-1])
            seznam.append(tupl)
        sql = "INSERT INTO dirkaci (did, ime, priimek, rojstvo, drzava) VALUES (?, ?, ?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()


def napolni_dirkalisca():
    '''Napolni tabelo dirkalisca'''
    with open("archive/circuits.csv", "r", encoding = 'utf-8') as dirkalisca:
        csv_reader = csv.reader(dirkalisca, delimiter=',')
        naslovi_st = next(csv_reader)
        seznam = []
        for vrstica in csv_reader:
            tupl = tuple([vrstica[0]] + vrstica[2:5])
            seznam.append(tupl)
        sql = "INSERT INTO dirkalisca (cid, ime, lokacija, drzava) VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()
        napolni_rezultati()
def napolni_dirka():
    '''Napolni tabelo dirka'''
    with open("archive/races.csv", "r") as dirka:
        csv_reader = csv.reader(dirka, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        for vrstica in csv_reader:
            tupl = tuple([vrstica[0], vrstica[3] ,vrstica[5]])
            seznam.append(tupl)
        sql = "INSERT INTO dirka (raceid, dirkalisce, datum) VALUES (?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()

def napolni_ekipa():
    '''Napolni tabelo ekipa'''
    with open("archive/constructors.csv", "r", encoding = 'utf-8') as ekipa:
        csv_reader = csv.reader(ekipa, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        for vrstica in csv_reader:
            tupl = tuple([vrstica[0], vrstica[2], vrstica[3]])
            seznam.append(tupl)
        sql = "INSERT INTO ekipa (eid, ime, drzava) VALUES (?, ?, ?)"
        cursor.executemany(sql, seznam)
        db.commit()
        
def napolni_rezultati():
    '''Napolni tabelo rezultati'''
    with open("archive/results.csv", "r", encoding="utf-8") as rezultati:
        csv_reader = csv.reader(rezultati, delimiter = ',')
        naslovi_st = next(csv_reader)
        seznam = []
        for vrstica in csv_reader:
            tupl = tuple([vrstica[1], vrstica[2], vrstica[3], vrstica[8], vrstica[9]])
            seznam.append(tupl)
        sql = 'INSERT INTO rezultati (rid, did, cid, pozicija, tocke) VALUES (?, ?, ?, ?, ?)'
        cursor.executemany(sql, seznam)
        db.commit()

dirkaci = "CREATE TABLE IF NOT EXISTS dirkaci (did INTEGER PRIMARY KEY, ime TEXT, priimek TEXT, rojstvo DATE, drzava TEXT)"

dirkalisca = "CREATE TABLE IF NOT EXISTS dirkalisca (cid INTEGER PRIMARY KEY, ime TEXT, lokacija TEXT, drzava TEXT)"

dirka = "CREATE TABLE IF NOT EXISTS dirka (raceid INTEGER PRIMARY KEY, dirkalisce INTEGER, datum DATE, FOREIGN KEY(dirkalisce) REFERENCES dirkalisca(cid))"

ekipa = "CREATE TABLE IF NOT EXISTS ekipa (eid INTEGER PRIMARY KEY, ime TEXT, drzava TEXT)"

#sezona = "CREATE TABLE IF NOT EXISTS sezona ()"

rezultati = "CREATE TABLE IF NOT EXISTS rezultati (rid INTEGER, did INTEGER, cid INTEGER, pozicija INTEGER, tocke INTEGER, FOREIGN KEY(rid) REFERENCES dirka(raceid), FOREIGN KEY(did) REFERENCES dirkaci(did), FOREIGN KEY(cid) REFERENCES ekipa(eid))"

# cid = constructorid
db = sqlite3.connect("f1database.sqlite3")

with db as cursor:
    cursor.execute(dirkaci)
    cursor.execute(dirkalisca)
    cursor.execute(dirka)
    cursor.execute(ekipa)
    cursor.execute(rezultati)
    napolni_dirkaci()
    napolni_dirkalisca()
    napolni_dirka()
    napolni_ekipa()
    napolni_rezultati()

