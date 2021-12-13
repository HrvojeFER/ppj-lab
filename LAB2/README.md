# Prevođenje programskih jezika - 2. laboratorijska vježba

- Sažetak:

    Izrada sintaksnog analizatora u formi pojednostavljenog programa Yacc korištenjem LR(1) parsera.
    
- Napomena:

    Neovisna vježba od 1. laboratorijske vježbe.
    

# Zadaci

- Generator sintaksnog analizatora

    - Opis ulazne datoteke
    
        %V nezavršni_znakovi_gramatike
        
        %T završni_znakovi_gramatike
        
        %Syn sinkronizacijski_završni_znakovi
        
        produkcije_gramatike
    
    - Opis nezavršnih znakova gramatike
        - točno jedan razmak nakon %V
        - neograničen broj NZ gramatike odvojenih jednim razmakom (" ")
        - NZ gramatike odgovara izrazu <([A-Z]|[a-z]|_)+>
        - prvi navedeni znak je početni NZ gramatike
        - primjer: "%V <NZJEDAN> <NZ_dva> <nZ_tRi>"
        
    - Opis završnih znakova gramatike
        - točno jedan razmak nakon %T
        - neograničen broj ZZ gramatike odvojenih jednim razmakom (" ")
        - ZZ gramatike odgovara izrazu ([A-Z]|[a-z]|_)+
        - primjer: "%T ZZJEDAN ZZ_dva zZ_tRi"
        
    - Opis sinkronizacijskih završnih znakova
        - točno jedan razmak nakon %Syn
        - neograničen broj SZ odvojen rednim razmakom (" ")
        - SZ gramatike odgovara izrazu {ZZ gramatike}
        - primjer: "%Syn ZZJEDAN zZ_tRi"
        
    - Opis produkcija gramatike
        - lijeva strana produkcije odgovara izrazu {NZ gramatike}
        - desna strana produkcije odgovara izrazu (\n {NZ gramatike}|{ZZ gramatike}|$)+, gdje se znak "$" koristi za epsilon prijelaz
        
- Sintaksni analizator

    - Opis ulazne datoteke
    
        ({uniformni_znak} redak_u_kojem_se_nalazi izraz)+
        
    - Treba se generirati generativno stablo
    
    - Ispis se radi DFS-om u obliku koji je u 3.3. u uputama
    
    - Finalni ispis treba biti s ispravljenom pogreškom
    
    
# Podjela posla

Za ovu lab. vježbu, postoji par cjelina koji se smatraju zadacima. Ova datoteka će se ažurirati kako ti zadaci nisu rješeni. Kad uzmete neki zadatak, stavite ime i datum kad ste ga uzeli pored tako da na istom zadatku ne radi više od 1 osobe. Nakon što je zadatak gotov, ime i datum se brišu i pored zadatka se stavlja zastavica "RIJEŠEN". Članovi tima uzimaju slobodne zadatke i na njima rade.

- Parser ulazne datoteke generatora sintaksnog analizatora **RIJEŠEN**
- Generacija tablica Akcija i NovoStanje LR(1) parsera (str 140, str. 148+) (Hrvoje 1.12.2018.)
- Izgradnja ɛ-NKA uz računanje ZAPOČINJE skupova (str. 102) **RIJEŠEN**
- Pretvorba dobivenog ɛ-NKA u minimizirani DKA (može se koristiti labos iz UTR) (Miljenko 1.12.2018.)
- Razrješavanje nejednoznačnosti (pročitaj na str. 31 upute)

---

- Parser ulazne datoteke sintaksnog analizatora **RIJEŠEN**
- Generator generativnog stabla za ulaz (za prethodno generirani sintaksni analizator)
- Ispravljač sintaksne pogreške

# Finalizacija

Generator sintaksnog analizatora se treba zvati GSA.py. Generirani sintaksni analizator se treba nalaziti u datoteci "analizator" pod nazivom SA.py
    