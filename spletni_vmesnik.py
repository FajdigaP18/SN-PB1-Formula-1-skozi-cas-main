from bottle import *
import model


# glavni_modeli
dirkaci_model = model.Dirkac()
dirkalisca_model = model.Dirkalisce()
ekipa_model = model.Ekipa()


# število elementov na strani
velikost_strani = 40

@route("/static/img/<filename>")
def serve_static_files_img(filename):
    return static_file(
        filename, root="./static/img"
    )

@route("/static/css/<filename>")
def serve_static_files_css(filename):
    return static_file(
        filename, root="./static/css"
    )

@get("/")
def glavna_stran():
    return template("template/glavna.html")

@get("/dirkaci")
def dirkaci_stran():
    '''Pridobimo podatke dirkačev'''

    stran = int(request.query.get('page', '1'))
    offset = (stran - 1) * velikost_strani
    limit = velikost_strani
    # vseh dirkačev je 855
    st_strani = (855 + velikost_strani - 1) // velikost_strani

    podatki = dirkaci_model.vsi_dirkaci(limit, offset)

    return template("template/dirkaci.html", dirkaci=podatki,  st_strani=st_strani, trenutna_stran=stran)

@get("/dirkaci/<did:int>")
def dirkaci_detajli(did):
    '''Za posameznega dirkača z identifikacijsko številko did pridobimo podatke'''
    dirkac = dirkaci_model.dobi_dirkaca(did)
    vse_ekipe = dirkaci_model.vse_ekipe(did)
    najbol_uvrstitve = dirkaci_model.najboljse_uvrstitve(dirkac.ime, dirkac.priimek)
    zmag_oder = dirkaci_model.zmagovalni_oder(did) 
    datum = dirkaci_model.dobi_dirkaca(did).rojstvo
    drzav = dirkaci_model.dobi_dirkaca(did).drzava
    if did in [1, 4, 807, 815, 817, 822, 825, 830, 832, 839, 840, 842, 844, 846, 847, 848, 849, 852, 854, 855]:
        return template("template/dirkacP.html", dirkac=dirkac, ekipe=vse_ekipe, uvrstitve=najbol_uvrstitve, oder=zmag_oder, d=datum, drzavljanstvo=drzav, did=did)
    return template("template/dirkac_detaili.html", dirkac=dirkac, ekipe=vse_ekipe, uvrstitve=najbol_uvrstitve, oder=zmag_oder, d=datum, drzavljanstvo=drzav)

## novo
@get("/dirkaci/<stolpec>")
def urejanje_dirkac(stolpec):
    '''Uredimo dirkače po velikosti glede na izbran stolpec.'''
    trenutna_stran= int(request.query.get('page', '1'))
    offset = (trenutna_stran - 1) * velikost_strani
    
    st_strani = (855 + velikost_strani - 1) // velikost_strani
    
    st= stolpec[0:-1]
    nar = True
    if stolpec[-1] == 'd':
        nar = False
    podatki = dirkaci_model.vsi_dirkaci2(velikost_strani, offset, uredi = st, narascajoce= nar)
    return template("template/dirkaci.html", dirkaci=podatki,  trenutna_stran=trenutna_stran, st_strani=st_strani)
##

@get("/dirkaci/iskanje")
def iskanje_dirkaci():
    #ime, priimek, drzava, datum, letnica ('', '', '', '', '')
    priimek = str(request.query.get("priimek"))
    ime = str(request.query.get("ime"))
    drzava = str(request.query.get("drzava"))
    datum = str(request.query.get("datum"))
    letnica = str(request.query.get("letnica"))
    dirkaci = dirkaci_model.iskanje_dirkaci(priimek=priimek , ime=ime, drzava=drzava, datum=datum, letnica=letnica)
    return template("template/dirkaci.html", dirkaci=dirkaci, trenutna_stran=1, st_strani=1)

@get("/dirkalisca")
def dirkalisca_stran():
    trenutna_stran= int(request.query.get('page', '1'))
    offset = (trenutna_stran - 1) * velikost_strani
    # vseh dirkališč je 76
    st_strani = (76 + velikost_strani- 1) // velikost_strani
    dirkalisca = dirkalisca_model.pridobi_vsa_dirkalisca(limit= velikost_strani, offset= offset)
    return template("template/dirkalisca.html", dirkalisca=dirkalisca, trenutna_stran=trenutna_stran, st_strani=st_strani)

##novo 
@get("/dirkalisca/<did:int>")
def dirkalisca_detajli(did):
    dirkalisce = dirkalisca_model.pridobi_dirkalisce(did)
    kdo = dirkalisca_model.kdo_najveckrat_zmagal(did)
    return template("template/dirkalisce_detaili.html", kdo = kdo, dirkalisce=dirkalisce)

#novo
@get("/dirkalisca/<stolpec>")
def urejena_dirkalisca(stolpec):
    trenutna_stran= int(request.query.get('page', '1'))
    offset = (trenutna_stran - 1) * velikost_strani
    # vseh dirkališč je 76
    st_strani = (76 + velikost_strani- 1) // velikost_strani
    nar = True
    st = stolpec[0:-1]
    if stolpec[-1] == 'd':
        nar = False
    dirkalisca = dirkalisca_model.pridobi_vsa_urejena_dirkalisca(limit = velikost_strani, offset = offset, uredi = st, narascajoce=nar)
    return template("template/dirkalisca.html", st_strani=st_strani, dirkalisca= dirkalisca, trenutna_stran=trenutna_stran)



@get("/ekipa")
def ekipa_stran():
    trenutna_stran= int(request.query.get('page', '1'))
    offset = (trenutna_stran - 1) * velikost_strani
    # vseh ekip je 211
    st_strani = (211 + velikost_strani- 1) // velikost_strani
    podatki = ekipa_model.pridobi_vse_ekipe(velikost_strani, offset)

    return template("template/ekipa.html", ekipe=podatki, st_strani = st_strani, trenutna_stran=trenutna_stran)

@get("/ekipa/<eid:int>")
def ekipe_detajli(eid):
    if eid in [131, 9, 6, 117, 1, 214, 3, 210, 51, 213]:
        return stran_posamezne_ekipe(eid)
    else:
        ekipa = ekipa_model.pridobi_ekipo(eid)
        dirkaci = ekipa_model.ekipa_vsi_dirkaci(eid)
        sezone = ekipa_model.ekipa_sezone(eid)
        return template("template/ekipa_detaili.html", ekipa=ekipa, dirkaci=dirkaci, sezone=sezone)

@get("/ekipa/iskanje")
def iskanje_ekipa():

    isci = str(request.query.get("isci"))
    ekipa = ekipa_model.iskanje_ekipe(isci)
    return template("template/ekipe_iskanje.html", ekipa=ekipa)

# novo
@get("/ekipeP")
def stran_ekipe():
    ekipe = list(ekipa_model.ekipe_v_sezoni(2022))
    return template("template/ekipeP.html", ekipe= ekipe)
# novo
@get("/ekipeP/<cid:int>")
def stran_posamezne_ekipe(cid):
    ekipa = ekipa_model.pridobi_ekipo(cid)
    trenutna_dirkaca = list(ekipa_model.dirkaca_v_ekipi_v_sezoni(2022, cid))
    predhodnjiki = ekipa_model.predhodnjiki_ekip(cid)
    vsi_dirkaci = ekipa_model.ekipa_vsi_vozniki(ekipa)
    prvi_nastop = ekipa_model.ekipa_prvi_nastop(ekipa)
    return template("template/ekipe_detajli.html", ekipa = ekipa, dirkaca = trenutna_dirkaca, predhodnjiki = predhodnjiki, vsi_dirkaci = vsi_dirkaci, prvi_nastop = prvi_nastop)

@get("/ekipa/<stolpec>")
def urejene_ekipe(stolpec):
    trenutna_stran= int(request.query.get('page', '1'))
    offset = (trenutna_stran - 1) * velikost_strani
    # vseh dirkališč je 211
    st_strani = (211 + velikost_strani- 1) // velikost_strani
    nar = True
    st = stolpec[0:-1]
    if stolpec[-1] == 'd':
        nar = False
    ekipe = ekipa_model.uredimo_ekipe(velikost_strani, offset, uredi=st, narascajoce=nar)
    return template("template/ekipa.html", ekipe=ekipe, st_strani = st_strani, trenutna_stran=trenutna_stran )

run(debug=True, reloader=True)


