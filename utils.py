import pandas as pd

def lue_csv_tiedosto(polkutiedosto, tuhaterotin=None, desimaalierotin='.'):
    """Lue CSV-tiedosto pandasilla, mahdollistaen tuhaterotin ja desimaalierotin"""
    kwargs = {}
    if tuhaterotin:
        kwargs['thousands'] = tuhaterotin
    if desimaalierotin:
        kwargs['decimal'] = desimaalierotin
    return pd.read_csv(polkutiedosto, **kwargs)

def sarakearvotNumeroiksi(df, sarake):
    """Muuntaa DataFrame-sarakkeen arvot kokonaisluvuiksi"""
    df[sarake] = pd.to_numeric(df[sarake], errors='coerce')
    return df



def pilkkupois(df, sarake):
    """Poistaa tuhaterottimet annetusta sarakkeesta ja muuntaa sen kokonaisluvuksi"""
    df[sarake] = df[sarake].astype(str).str.replace(',', '')
    return df

#luetaan vain sarakkeet jossa sama Projekti
def lue_csv_tiedosto_projekti(polkutiedosto, projekti, tuhaterotin=None, desimaalierotin='.'):
    """Lue CSV-tiedosto pandasilla, suodattaa projekti-sarakkeen mukaan"""
    df = lue_csv_tiedosto(polkutiedosto, tuhaterotin, desimaalierotin)
    return df[df['Projekti'] == projekti]

#luetaan vain sarake
def luetaan_vain_sarake(df, sarakeNimi, arvo):
    """Lue DataFrame ja suodata vain ne rivit, joissa sarakkeen arvo on tietty"""
    tempdf = df[df[sarakeNimi] == arvo]
    return tempdf


# lisätään uusi sarake tauluun
def lisaa_uusi_sarake(df, sarake_nimi, arvo):
    """Lisää uuden sarakkeen tauluun"""
    df[sarake_nimi] = arvo
    return df


# Lisätään brutto-sarake
def lisaa_brutto_sarake(df, sarake):
    """Lisää arvot valitulle sarakkeelle joka on Debet-sarakkeen arvojen 1.25-kertainen"""
    if sarake in df.columns:
    #loop through the DataFrame and multiply the 'Debet' column by 1.25
        df[sarake] = df['Kredit'].apply(lambda x: x * 1.25 if x > 0 else x)

    else:   
        print(f"Saraketta '{sarake}' ei löydy DataFrame:stä.")
    #return the modified DataFrame
    return df

# vaihdetaan sarake arvoja toiseen sarakkeeseen
def vaihda_sarake_arvot(df, vanha_sarake, uusi_sarake):
    """Vaihdetaan sarake arvoja toiseen sarakkeeseen"""
    if vanha_sarake in df.columns:
        df[uusi_sarake] = df[vanha_sarake]
        #df.drop(columns=[vanha_sarake], inplace=True)
    else:
        print(f"Saraketta '{vanha_sarake}' ei löydy DataFrame:stä.")
    return df

#poistetaan sarake
def poista_sarake(df, sarake):
    """Poistetaan sarake DataFrame:stä"""
    if sarake in df.columns:
        df.drop(columns=[sarake], inplace=True)
    else:
        print(f"Saraketta '{sarake}' ei löydy DataFrame:stä.")
    return df

#tee dataframesta excel
def tallenna_excel(df, tiedostonimi):
    """Tallentaa DataFrame:n Excel-tiedostona"""
    df.to_excel(tiedostonimi, index=False)

#lisää exceli tiedostoon  5 riviä metatietoja
def lisaa_metatiedot_excel(df, tiedostonimi):
    """Lisää Excel-tiedostoon 5 riviä metatietoja"""
    metatiedot = pd.DataFrame({
        'Metatieto': ['Lähde', 'Päivämäärä', 'Versio', 'Tekijä', 'Kuvaus'],
        'Arvo': ['Lähde 1', '2023-01-01', '1.0', 'Tekijä 1', 'Kuvaus 1']
    })
    with pd.ExcelWriter(tiedostonimi, engine='openpyxl', mode='a') as writer:
        metatiedot.to_excel(writer, sheet_name='Metatiedot', index=False)