import utils
import pandas as pd

# Lue tiedosto
df = utils.lue_csv_tiedosto("inputdata.csv", tuhaterotin=",")

# Muokkaa sarake
df = utils.pilkkupois(df, "Debet")

print(df.head())

#muuteetaan sarake debet ja Kredit luvuiksi
df = utils.sarakearvotNumeroiksi(df, "Debet")
df = utils.sarakearvotNumeroiksi(df, "Kredit")
print(df.head())
# luetaan vain sarakkeet jossa sama Projekti
projekti_df = utils.lue_csv_tiedosto_projekti("inputdata.csv", "PRJ-001", tuhaterotin=",")
print(projekti_df.head())

# Lisätään uusi sarake tauluun
df = utils.lisaa_uusi_sarake(df, "Brutto", 0)

print(df.head())

# Lisätään brutto-sarake, joka on Debet-sarakkeen arvojen 1.25-kertainen
df = utils.lisaa_brutto_sarake(df, "Brutto")
print(df.head())

# Vaihdetaan sarake arvoja toiseen sarakkeeseen
#df = utils.vaihda_sarake_arvot(df, "Valuutta", "Kredit")
#print(df.head())
