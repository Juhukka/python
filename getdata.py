import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os

load_dotenv()  # Lataa ympäristömuuttujat .env-tiedostosta, jos käytössä

print(os.getenv("API_KEY"))  # Tulostaa API-avaimen, jos se on määritelty .env-tiedostossa
token = os.getenv("API_KEY")  # Korvataan omalla tokenilla

gitkayttaja = "Juhukka"
repo = "python"
filename = "inputdata.csv"
# GitHub-tiedoston API-osoite (raw endpoint toimii vain julkisille)
api_url = f"https://api.github.com/repos/{gitkayttaja}/{repo}/contents/{filename}"


headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.raw+json"
}

"""
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3.raw"
}
"""


response = requests.get(api_url, headers=headers)

# Muunna CSV pandasille
if response.status_code == 200:
    csv_string = response.text
    df = pd.read_csv(StringIO(csv_string))
    print(df.head())
else:
    print("Virhe:", response.status_code)