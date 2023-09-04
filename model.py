import sqlite3


conn = sqlite3.connect("f1database.sqlite3")


# vir : https://wtf1.com/post/these-are-all-the-f1-team-changes-in-the-last-decade/
# vir : https://www.topgear.com/car-news/formula-one/formula-one-here-are-family-trees-every-team

nove_ekipe = {
    'Mercedes': ('Mercedes', 'Tyrrell', 'BAR', 'Honda', 'Brawn'), 
    'Red Bull':('Red Bul Racing', 'Jaguar', 'Stewart', 'Red Bull'),
    'Ferrari': ('Ferrari'),
    'Aston Martin': ('Aston Martin', 'Jordan','Spyker', 'Spyker MF1','Force India','Racing Point', 'Spyker MF1'), 
    'McLaren': ('McLaren'), 
    'Alpine F1 Team': ('Alpine', 'Toleman','Benetton','Renault','Lotus','Lotus F1', 'Caterham','Alpine F1 Team', 'Lotus-Pratt &amp; Whitney', 'Team Lotus'), 
    'Williams': ('Williams', 'Wolf'),
    'Haas F1 Team': ('Haas F1 Team', 'Marussia', 'Manor Marussia','Virgin'),
    'Alfa Romeo': ('Alfa Romeo', 'Sauber','Brabham-Alfa Romeo', 'March-Alfa Romeo', 'McLaren-Alfa Romeo', 'BMW Sauber', 'March' ),
    'AlphaTauri':('Minardi', 'Toro Rosso', 'AlphaTauri' )
}
ekipe_2022 = [131, 9, 6, 117, 1, 214, 3, 210, 51, 213]
ekipe_2022_1 = ['Mercedes', 'Red Bull', 'Ferrari', 'Aston Martin', 'McLaren', 'Alpine F1 Team', 'Williams', 'Haas F1 Team', 'Alfa Romeo','AlphaTauri']

      
class Dirkac:
    
    def __init__(self, ide=None, ime=None, priimek=None, drzava = None, rojstvo = None):
        self.id = ide
        self.ime = ime
        self.priimek = priimek
        self.drzava = drzava
        self.rojstvo = rojstvo
        
    def __str__(self):
        return f'{self.ime} {self.priimek}'


    @staticmethod
    def dobi_dirkaca(did):
        with conn:
            cursor = conn.execute("""
                SELECT did, ime, priimek, drzava, rojstvo
                FROM dirkaci
                WHERE did=?
            """, [did])
            podatki = cursor.fetchone()
            return Dirkac(podatki[0], podatki[1], podatki[2], podatki[3], podatki[4])
    
    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Dirkac(*poizvedba)
            
    @staticmethod
    def vsi_dirkaci(limit, offset):
        '''Pridobi vse dirkace'''
        sql = '''SELECT ime,
                     priimek,
                     dirkaci.drzava,
                     dirkaci.rojstvo,
                     did
                FROM dirkaci LIMIT ? OFFSET ?'''
        vsi_dirkaci = conn.execute(sql, (limit, offset)).fetchall()
        for dirkac in vsi_dirkaci:
            yield dirkac
    
    ## novo 
    @staticmethod
    def vsi_dirkaci2(limit, offset, uredi= 'did', narascajoce = True):
        ''' Poišče vse dirkače in jih uredi po Imenu, Priimku, Datumu rojstva ali po narodnosti.'''
        if not uredi in {'ime', 'priimek', 'drzava', 'rojstvo', 'did'}:
            return 
        if not narascajoce:
            uredi += ' DESC'
        sql = '''SELECT ime,
                     priimek,
                     dirkaci.drzava,
                     dirkaci.rojstvo,
                     did
                FROM dirkaci
                ORDER BY {}
                LIMIT ? OFFSET ?'''.format(uredi)
        vsi_dirkaci = conn.execute(sql, (limit, offset)).fetchall()
        for dirkac in vsi_dirkaci:
            yield dirkac
    ##

    @staticmethod
    def vse_ekipe(did):
        '''Poda tabelo vseh ekip v katerih je dirkal dirkač.'''
        sql = '''SELECT DISTINCT ekipa.ime, ekipa.eid
                         FROM ekipa
                              INNER JOIN
                              rezultati ON ekipa.eid = rezultati.cid
                              INNER JOIN
                              dirkaci ON dirkaci.did = rezultati.did
                        WHERE dirkaci.did = ?'''

        ekipe = conn.execute(sql,[did]).fetchall()
        for ekipa in ekipe:
            yield ekipa

    # najboljša uvrstitev
    @staticmethod
    def najboljse_uvrstitve(ime, priimek):
        '''Poda podatke najboljše uvrstitve dirkača.'''
        sql = '''SELECT DISTINCT dirkalisca.cid, dirkaci.ime,
                              dirkaci.priimek,
                              rezultati.pozicija,
                              ekipa.ime,
                              dirkalisca.ime,
                              dirka.datum,
                              ekipa.eid
                         FROM dirkaci
                              INNER JOIN
                              rezultati ON dirkaci.did = rezultati.did
                              INNER JOIN
                              ekipa ON ekipa.eid = rezultati.cid
                              INNER JOIN
                              dirka ON dirka.raceid = rezultati.rid
                              INNER JOIN
                              dirkalisca ON dirka.dirkalisce = dirkalisca.cid
                        WHERE dirkaci.ime = ? AND 
                              dirkaci.priimek = ? AND 
                              rezultati.pozicija = (
                                                       SELECT min(rezultati.pozicija) 
                                                         FROM rezultati
                                                        GROUP BY rezultati.did
                                                       HAVING rezultati.did = (
                                                                                  SELECT dirkaci.did
                                                                                    FROM dirkaci
                                                                                   WHERE dirkaci.ime = ? AND 
                                                                                         dirkaci.priimek = ?
                                                                              )
                                                   )
                        ORDER BY dirka.datum DESC;'''

        podatki = (ime, priimek, ime, priimek)
        yield conn.execute(sql, podatki).fetchall()

        
    # Koliko uvrstitev na zmagovalni oder
    @staticmethod
    def zmagovalni_oder(did):
        '''Poda stevilo uvrstitev dirkaca na zmagovalni oder.'''
        sql = '''SELECT dirkaci.ime,
                               dirkaci.priimek,
                               count( * ) AS oder_za_zmagovalce,
                               dirkaci.rojstvo,
                               dirkaci.drzava
                          FROM dirkaci
                               INNER JOIN
                               rezultati ON dirkaci.did = rezultati.did
                         WHERE rezultati.pozicija < 4
                         GROUP BY dirkaci.did
                        HAVING dirkaci.did = ?'''
        yield conn.execute(sql, [did]).fetchone()

    @staticmethod
    def iskanje_dirkaci(priimek= '', ime = '',  drzava = '', datum = '', letnica = ''):
        '''Poiščemo po dirkačih glede  na državo, rojstvo, ime, priimek ali pa did'''
        sql ="""
            SELECT priimek, ime, drzava, rojstvo, did
            FROM dirkaci 
            WHERE priimek LIKE ? 
            UNION 
            SELECT priimek, ime, drzava, rojstvo, did
            FROM dirkaci 
            WHERE ime LIKE ?
            UNION 
            SELECT priimek, ime, drzava, rojstvo, did
            FROM dirkaci 
            WHERE drzava LIKE ?
            UNION 
            SELECT priimek, ime, drzava, rojstvo, did
            FROM dirkaci 
            WHERE rojstvo LIKE ?
            UNION
            SELECT priimek, ime, drzava, rojstvo, did
            FROM dirkaci
            WHERE strftime('%Y', rojstvo) = ?;
            """
        isci = datum.split('.')
        if len(isci) == 3:
            datum = f"{isci[-1]}-{isci[1]}-{isci[0]}"
        podatki  = conn.execute(sql, [priimek, ime, drzava, datum, letnica]).fetchall()
        for dirkac in podatki:
            yield dirkac


    
class Ekipa:

    def __init__(self, eid=None, ime=None, nationality=None):
        self.eid = eid
        self.ime = ime
        self.nationality = nationality

    def __str__(self) -> str:
        return str(self.ime)
    
    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Ekipa(*poizvedba)

    @staticmethod
    def pridobi_vse_ekipe(limit, offset):
        sql = '''
                SELECT eid, ime, drzava
                FROM ekipa
                ORDER BY ime
                LIMIT ? OFFSET ?;'''
        ekipe = conn.execute(sql, [limit, offset]).fetchall()
        for ekipa in ekipe:
            yield ekipa
    # novo
    @staticmethod
    def uredimo_ekipe(limit, offset, uredi='eid', narascajoce = True):
        if not uredi in {'ime', 'drzava', 'eid'}:
            return 
        if not narascajoce:
            uredi += ' DESC'
        sql = '''
                SELECT eid, ime, drzava
                FROM ekipa
                ORDER BY {}
                LIMIT ? OFFSET ?;'''.format(uredi)
        ekipe = conn.execute(sql, [limit, offset]).fetchall()
        for ekipa in ekipe:
            yield ekipa

    @staticmethod
    def pridobi_vse_nemce():
        sql = '''
                SELECT eid, ime FROM ekipa
                WHERE drzava = 'German'
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa
    
    @staticmethod
    def pridobi_vse_angleze():
        sql = '''
                SELECT eid, ime FROM ekipa
                WHERE drzava = 'British'
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa
    
    @staticmethod
    def pridobi_vse_italijane():
        sql = '''
                SELECT eid, ime FROM ekipa
                WHERE drzava = 'Italian'
                ORDER BY ime;'''
        ekipe = conn.execute(sql).fetchall()
        for ekipa in ekipe:
            yield ekipa

    @staticmethod
    def poisci_po_imenu(ime, limit=None):
        sql = '''
            SELECT ime FROM ekipa
            WHERE ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Ekipa.poisci_sql(sql, podatki)

    @staticmethod
    def poisci_po_nacionalnosti(nacija, limit=None):
        sql = '''
            SELECT drzava FROM ekipa
            WHERE drzava LIKE ?'''
        podatki = ['%' + nacija + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Ekipa.poisci_sql(sql, podatki)
    
    @staticmethod
    def pridobi_ekipo(eid):
        sql = '''SELECT eid,
                      ime,
                      drzava
                 FROM ekipa
                WHERE eid = ?;
        '''
        podatki = conn.execute(sql, [eid]).fetchone()
        return Ekipa(podatki[0], podatki[1], podatki[2])
    
    @staticmethod
    def ekipa_vsi_dirkaci(eid):
        '''Pridobi vse dirkace, ki so dirkali za to ekipo.'''
        sql = '''SELECT DISTINCT dirkaci.ime,
                               dirkaci.priimek,
                               dirkaci.did
                 FROM dirkaci
                      INNER JOIN
                      rezultati ON dirkaci.did = rezultati.did
                      INNER JOIN
                      ekipa ON rezultati.cid = ekipa.eid
                WHERE ekipa.eid = ?;'''
        podatki = conn.execute(sql, [eid]).fetchall()
        for dirkac in podatki:
            yield dirkac

    @staticmethod
    def ekipa_sezone(eid):
        '''Pridobi vse sezone v katerih je sodelovala ta ekipa'''
        sql = '''SELECT tabela.leto  
                    FROM 
                        (SELECT DISTINCT cid as cid,
                                strftime('%Y', dirka.datum) AS leto
                            FROM rezultati
                        INNER JOIN
                        dirka ON dirka.raceid = rezultati.rid) tabela
                WHERE cid = ? ;'''
        podatki = conn.execute(sql, [eid]).fetchall()
        for leto in podatki:
            yield leto

    ## novo
    @staticmethod
    def ekipa_vsi_vozniki(ekipa):
        '''Pridobi vse voznike, ki so dirkali za to ekipo.'''
        sez = nove_ekipe[ekipa.ime]
        if (type(sez) != tuple):
            v_sql = ' == ?'
            sez = [f"{ekipa.ime}"]
            print(sez)
        else:
            vpra= '?'
            v_sql = ', '.join(vpra for _ in sez )
            v_sql = f" IN ({v_sql})"
        sql = f'''SELECT DISTINCT dirkaci.ime,
                               dirkaci.priimek,
                               dirkaci.did
                 FROM dirkaci
                      INNER JOIN
                      rezultati ON dirkaci.did = rezultati.did
                      INNER JOIN
                      ekipa ON rezultati.cid = ekipa.eid
                WHERE ekipa.ime {v_sql};'''
        podatki = conn.execute(sql, sez).fetchall()
        for dirkac in podatki:
            yield dirkac
    
    ## novo 
    @staticmethod
    def ekipa_prvi_nastop(ekipa):
        '''Pridobi letnico prvega nastopa na dirki f1'''
        sez = nove_ekipe[ekipa.ime]
        if (type(sez) != tuple):
            v_sql = ' == ?'
            sez = [f"{ekipa.ime}"]
        else:
            vpra= '?'
            v_sql = ', '.join(vpra for _ in sez )
            v_sql = f" IN ({v_sql})"
        sql = f'''SELECT tabela.leto 
                    FROM (
                        SELECT DISTINCT cid AS cid,
                           strftime('%Y', dirka.datum) AS leto
                        FROM rezultati
                        INNER JOIN
                        dirka ON dirka.raceid = rezultati.rid
                        )
                        tabela
                    WHERE cid IN (
                    SELECT eid
                    FROM ekipa
                    WHERE ekipa.ime {v_sql}
                    )
                    order by leto
                    limit 1 ;'''
        podatek = conn.execute(sql, sez).fetchone()
        return podatek

    ### novo
    @staticmethod
    def ekipe_v_sezoni(sezona):
        '''Pošče vse ekipe ki so sodelovale v sezoni sezona'''
        sql = '''SELECT DISTINCT ekipa.eid,
                    ekipa.ime AS IME
                        FROM (
                            SELECT dirka.raceid
                                FROM dirka
                                WHERE strftime('%Y', dirka.datum) = ?
                            )
                            f1
                            INNER JOIN
                            rezultati ON f1.raceid == rezultati.rid
                            INNER JOIN
                            ekipa ON ekipa.eid == rezultati.cid;'''
        podatki = conn.execute(sql, [f'{sezona}']).fetchall()
        for ekipa in podatki:
            yield ekipa
    # nova
    @staticmethod
    def dirkaca_v_ekipi_v_sezoni(sezona, ekipa):
        '''Poisce dirkaca v sezoni sezona in ekipo ekipa (id)'''
        sql = '''SELECT DISTINCT dirkaci.did, cid,
                ime,
                priimek,
                drzava,
                dirkaci.did
                FROM rezultati
                    INNER JOIN
                        (
                        SELECT raceid
                        FROM dirka
                         WHERE strftime('%Y', dirka.datum) = ?
                        LIMIT 1
                        )
                    ON raceid == rid
                    INNER JOIN
                dirkaci ON dirkaci.did == rezultati.did
                where cid == ?;'''
        podatki = conn.execute(sql, [f"{sezona}", f"{ekipa}"]).fetchall()
        for dirkac in podatki:
            yield dirkac
        
    ### nova
    @staticmethod
    def predhodnjiki_ekip(cid):
        '''Poišče vse predhodnike ekip ekipe ekipa'''
        sql = '''SELECT ime
                FROM ekipa
                WHERE eid == ?;'''
        podatki = conn.execute(sql,[cid]).fetchall()
        string = str()
        ekipe = nove_ekipe[podatki[0][0]]
        if type(ekipe) == tuple:
            for i in ekipe:
                string += f"{i}, "
        else:
            string = ekipe + ', '
        return string[:-2]

    # novo
    @staticmethod
    def iskanje_ekipe(isci):
        '''Poiscemo ekipo glede na ime ali pa drzavo'''
        sql ="""
            SELECT eid, ime, drzava 
            FROM ekipa 
            WHERE drzava LIKE ?;
            """
        podatki = conn.execute(sql, [isci]).fetchall()
        for ekipa in podatki:
            yield ekipa
    
            
class Dirkalisce:
    def __init__(self, cid=None, ime=None, drzava=None):
        self.id = cid
        self.ime = ime
        self.drzava = drzava
    
    def __str__(self):
        return str(self.ime)
    
    @staticmethod
    def poisci_sql(sql, podatki = None):
        for poizvedba in conn.execute(sql, podatki):
            yield Dirkalisce(*poizvedba)
            
    @staticmethod
    def pridobi_dirkalisce(cid):
        sql = '''SELECT dirkalisca.cid,
                      dirkalisca.ime,
                      dirkalisca.drzava
                 FROM dirkalisca
                WHERE cid = ?;'''
        podatki = conn.execute(sql, [cid]).fetchone()
        return Dirkalisce(podatki[0], podatki[1], podatki[2])
    
    @staticmethod
    def pridobi_vsa_dirkalisca(limit, offset):
        sql = '''
                SELECT cid, ime, lokacija, drzava FROM dirkalisca
                ORDER BY ime LIMIT ? OFFSET ?;'''
        vsa_dirkalisca = conn.execute(sql, (limit, offset)).fetchall()
        for dirkalisce in vsa_dirkalisca:
            yield dirkalisce
    
    # novo
    @staticmethod    
    def pridobi_vsa_urejena_dirkalisca(limit, offset, uredi= 'cid', narascajoce = True):
        ''' Poišče vse dirkače in jih uredi po Imenu, Priimku, Datumu rojstva ali po narodnosti.'''
        if not uredi in {'ime', 'lokacija', 'drzava', 'did'}:
            return 
        if not narascajoce:
            uredi += ' DESC'
        sql = '''SELECT cid,
                     ime,
                     lokacija,
                     drzava
                FROM dirkalisca
                ORDER BY {}
                LIMIT ? OFFSET ?'''.format(uredi)
        vsa_dirkalisca = conn.execute(sql, (limit, offset)).fetchall()
        for dirkalisce in vsa_dirkalisca:
            yield dirkalisce
    
    @staticmethod        
    def poisci_po_imenu(ime, limit=None):
        sql = '''
            SELECT ime FROM dirkalisca
            WHERE ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Dirkalisce.poisci_sql(sql, podatki)
    
    @staticmethod
    def najveckrat_zmagal():
        '''Poisce dirkalisce in osebo ki je najveckarat zmagala na tem dirkaliscu ter stevilo zmag.'''
        sql = '''SELECT tabela.proga,
                       tabela.ime,
                       tabela.priimek,
                       max(tabela.st) AS stevilo_zmag
                  FROM (
                           SELECT rezultati.did,
                                  dirkaci.did,
                                  dirkaci.ime AS ime,
                                  dirkaci.priimek AS priimek,
                                  dirka.dirkalisce,
                                  dirkalisca.cid,
                                  dirkalisca.ime AS proga,
                                  count( * ) AS st
                             FROM rezultati
                                  INNER JOIN
                                  dirka ON dirka.raceid = rezultati.rid
                                  INNER JOIN
                                  dirkalisca ON dirkalisca.cid = dirka.dirkalisce
                                  INNER JOIN
                                  dirkaci ON dirkaci.did = rezultati.did
                            WHERE rezultati.pozicija = 1
                            GROUP BY rezultati.did,
                                     dirka.dirkalisce
                       )
                       tabela
                 GROUP BY dirkalisce
                 order by tabela.proga;'''
        vsa_dirkalisca = conn.execute(sql).fetchall()
        for dirkalisce in vsa_dirkalisca:
            yield dirkalisce
    
    @staticmethod        
    def kdo_najveckrat_zmagal(proga_id):
        '''Pridobi podatke o tem kdo je na dirkaliscu prog_id najveckrat zmagal
        ter kolikokrat je zmagal (proga_id, ime_dirkalisca, kdo_ime, kdo_priimek, st_zmag)'''  
        sql = '''SELECT tabela1.proga_id,
                       tabela1.proga,
                       tabela1.najboljsi_ime,
                       tabela1.najboljsi_priimek,
                       tabela1.stevilo_zmag,
                       tabela1.najboljsi_id
                  FROM (
                           SELECT tabela.proga_id AS proga_id,
                                  tabela.proga AS proga,
                                  tabela.ime AS najboljsi_ime,
                                  tabela.priimek AS najboljsi_priimek,
                                  max(tabela.st) AS stevilo_zmag,
                                  tabela.did AS najboljsi_id
                             FROM (
                                      SELECT rezultati.did,
                                             dirkaci.did AS did,
                                             dirkaci.ime AS ime,
                                             dirkaci.priimek AS priimek,
                                             dirka.dirkalisce,
                                             dirkalisca.cid AS proga_id,
                                             dirkalisca.ime AS proga,
                                             count( * ) AS st
                                        FROM rezultati
                                             INNER JOIN
                                             dirka ON dirka.raceid = rezultati.rid
                                             INNER JOIN
                                             dirkalisca ON dirkalisca.cid = dirka.dirkalisce
                                             INNER JOIN
                                             dirkaci ON dirkaci.did = rezultati.did
                                       WHERE rezultati.pozicija = 1
                                       GROUP BY rezultati.did,
                                                dirka.dirkalisce
                                  )
                                  tabela
                            GROUP BY dirkalisce
                            ORDER BY tabela.proga
                       )
                       tabela1
                 WHERE tabela1.proga_id = ?;''' 
        podatki = conn.execute(sql, [proga_id]).fetchone()
        yield podatki



class Sezona:
    def __init__(self, leto=None):
        self.leto = leto
        
    def __str__(self):
        return self.leto
    
    @staticmethod
    def poisci_sql(sql, podatki = None):
        for poizvedba in conn.execute(sql, podatki):
            yield Sezona(*poizvedba)
    
    @staticmethod
    def pridobi_vse_sezone():
        '''Poisce vse sezone.'''
        sql = '''
                SELECT DISTINCT strftime('%Y', dirka.datum) AS leto
                  FROM dirka
                 ORDER BY leto DESC;'''
        vse_sezone = conn.execute(sql).fetchall()
        for sezona in vse_sezone:
            yield sezona
            
    @staticmethod
    def rezultati_sezona(sezona):
        '''Pridobi koncne rezultate sezone.'''
        sql = '''SELECT rezultati.did,
                      dirkaci.ime,
                      dirkaci.priimek,
                      sum(rezultati.tocke) AS tocke
                 FROM rezultati
                      inner JOIN
                      dirkaci ON rezultati.did = dirkaci.did
                      INNER JOIN
                      dirka ON dirka.raceid = rezultati.rid
                WHERE strftime('%Y', dirka.datum) = ?
                GROUP BY rezultati.did
                ORDER BY tocke DESC;'''
        vsi_rezultati = conn.execute(sql, sezona).fetchall()
        for rezultat in vsi_rezultati:
            yield rezultat
    

    