import model 
# Poženite program

# glavni_modeli
dirkaci_model = model.Dirkac()
dirkalisca_model = model.Dirkalisce()
ekipa_model = model.Ekipa()

prekinitev = "_"*100
velikost_strani = 10
def testiramo_program():
    '''Program ki pokaže najboljšefunkcionalnosti spletnega vmesnega.'''
    print("Za brskanje po dirkačih vtipkajte 1. ")
    print("Za brskanje po prizoriščih vtipkajte 2. ")
    print("Za brskanje po ekipah vtipkajte 3. ")
    print("Za zaključek delovanja programa pritisnite 4.")
    
    print(prekinitev)
    try:
        uporabnik = int(input("Želim izvesti številko: "))

        # Dirkaci
        if uporabnik == 1:
            # poiscemo npr 10 dirkacev ki so urejeni po priimku imenu bla bla
            print("")
            print("Urejamo lahko po {'ime', 'priimek', 'drzava', 'rojstvo', 'did'}")
            uredimo_po = input("Izberi način urejanja: ")
            uredimo_nar = input("Za padajoče urejanje podatkov vpišite False, za naraščajoče pa True. ")
            nar = True
            if uredimo_nar == 'False':
                nar = False 
            st_strani = (855 + velikost_strani - 1) // velikost_strani
            trenutna_stran = int(input(f"Izberi stran na kateri se nahajamo (izberi število med 1 in {st_strani}): "))
            podatki = dirkaci_model.vsi_dirkaci2(velikost_strani, st_strani, uredi = uredimo_po, narascajoce= uredimo_nar)
            print(" {:{odmik1}} | {:{odmik2}} | {:{odmik2}} | {:{odmik3}} | {}".format('id', 'priimek', 'ime', 'nacionalnost', 'datum rojstva', odmik1 = 3, odmik2 = 20, odmik3 = 15))
            print('-'*100)
            for dirkac in podatki:
                print(f"{dirkac[4]:{4}} | {dirkac[1]:{20}} | {dirkac[0]:{20}} | {dirkac[2]:{15}} | {dirkac[3]}")
            print(prekinitev)
        
            id_dirkaca = int(input("Izberi id dirkača: "))
        
            dirkac = dirkaci_model.dobi_dirkaca(id_dirkaca)
            vse_ekipe = dirkaci_model.vse_ekipe(id_dirkaca)
            ekipe = ''
            for i in vse_ekipe:
                ekipe += f"{i} "
            datum = dirkaci_model.dobi_dirkaca(id_dirkaca).rojstvo
            drzav = dirkaci_model.dobi_dirkaca(id_dirkaca).drzava
            print(f"Izbrani dirkac {id_dirkaca}: {dirkac}")
            print(f"Vse ekipe v katerih je dirkac dirkal {ekipe}")
            print(f"Datum rojstva : {datum}")
            print(f"Državljanstvo : {drzav}")
            nadaljuj = input("Če želite nadaljevati vpišite da, drugače pa ne. ")
            if nadaljuj == 'da':
                testiramo_program()
            else:
                return 

        # Prizorišča
        elif uporabnik == 2:
            print("DIRKALIŠČA:")
            print('='*100)
            print("")
            print("Urejamo lahko po {'ime', 'lokacija', 'drzava', 'did'}")
            uredimo_po = input("Izberi način urejanja: ")
            uredimo_nar = input("Za padajoče urejanje podatkov vpišite False, za naraščajoče pa True. ")
            nar = True
            if uredimo_nar == 'False':
                nar = False 
            st_strani = (79 + velikost_strani - 1) // velikost_strani 
            trenutna_stran = int(input(f"Izberi stran na kateri se nahajamo (izberi število med 1 in {st_strani}): "))
        
            dirkalisca = dirkalisca_model.pridobi_vsa_urejena_dirkalisca(velikost_strani, st_strani, uredi = uredimo_po, narascajoce=nar)
            print("{:{odmik1}} | {:{odmik2}} | {:{odmik3}} | {}".format('id', 'ime', 'lokacija', 'država', odmik1 = 4, odmik2 = 40, odmik3 = 20))
            print('-'*100)
            for dirkalisce in dirkalisca:
                print(f"{dirkalisce[0]:{4}} | {dirkalisce[1]:{40}} | {dirkalisce[2]:{20}} | {dirkalisce[3]}")
            print(prekinitev)
            did = int(input("izberite id dirkališča: "))
            did_dirkalisce = dirkalisca_model.pridobi_dirkalisce(did)
            dirkac = dirkalisca_model.pridobi_vsa_dirkalisca(50, 1)
            niz_kdo = ''
            kdo = dirkalisca_model.kdo_najveckrat_zmagal(did)
        
            print(f"Izbrano dirkališe z id {did} je {did_dirkalisce}.")
            for n in kdo:
                print(f"{n[2]} {n[3]} je osvojil { n[4]} zmag.")
        
            print(prekinitev)
            nadaljuj = input("Če želite nadaljevati vpišite da, drugače pa ne. ")
            if nadaljuj == 'da':
                testiramo_program()
            else:
                return 


        # Ekipe
        elif uporabnik == 3:
            print("EKIPE")
            ekipe = ekipa_model.ekipe_v_sezoni(2022)
            print("{:{odmik}} | ekipe".format('id', odmik = 4))
            print('-'*100)
            for e in ekipe:
                print(f"{e[0]:{4}} | {e[1]}")
            print(prekinitev)
            cid = int(input("Izberite eno izmed id ekipe: "))
            ekipa = ekipa_model.pridobi_ekipo(cid)
            print("Dirkaca v sezoni 2022:")
            trenutna_dirkaca = ekipa_model.dirkaca_v_ekipi_v_sezoni(2022, cid)
            for dirkac in trenutna_dirkaca:
                print(f"- {dirkac[2]} {dirkac[3]}")
            print(prekinitev)
            prvi_nastop = ekipa_model.ekipa_prvi_nastop(ekipa)
            print(f"Prvi nastop ekipe na dirki f1 je bil leta {prvi_nastop[0]}. ")
        
            ekipe = ekipa_model.predhodnjiki_ekip(cid)
            print(f" Predhodnje ekipe: {ekipe}.")

            nadaljuj = input("Če želite nadaljevati vpišite da, drugače pa ne. ")
            if nadaljuj == 'da':
                testiramo_program()
            else:
                return
        
        # Konec funkcije
        elif uporabnik == 4:
            return
    
        else:
            print(prekinitev)
            print()
            print("Izbrati morate eno od števil zgoraj.")
            print()
            nadaljuj = input("Če želite nadaljevati vpišite da, drugače pa ne. ")
            if nadaljuj == 'da':
                testiramo_program()
            else:
                return
    except:
        print("Izbrati morate eno izmed številk.")
        print(prekinitev)
        testiramo_program()
    

testiramo_program()

