import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os
import base64

load_dotenv()  # Lataa ympäristömuuttujat .env-tiedostosta, jos käytössä

print(os.getenv("API_KEY"))  # Tulostaa API-avaimen, jos se on määritelty .env-tiedostossa
token = os.getenv("API_KEY")  # Korvataan omalla tokenilla

gitkayttaja = "Juhukka"
repo = "python"
LOCAL_FILE = "inputdata.csv"
filename = "inputdatav2.csv"
#luetaan tiedosto binaaarisena
with open(LOCAL_FILE, "rb") as f:
    content = f.read()
    encoded_content = base64.b64encode(content).decode()

# GitHub-tiedoston API-osoite (raw endpoint toimii vain julkisille)
api_url = f"https://api.github.com/repos/{gitkayttaja}/{repo}/contents/{filename}"


headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

params = {"ref" : "main"}

response = requests.get(api_url, headers=headers, params=params)

sha = None
if response.status_code == 200:
    # Haetaan tiedoston SHA, jos se on olemassa
    file_info = response.json()
    sha = file_info.get('sha', None)
    if sha:
        print(f"Tiedoston SHA: {sha}")
    else:
        print("SHA-tietoa ei löytynyt.")


data = {
    "message": "lisätään tiedosto",
    "content": encoded_content,
    "branch": "main",
}

if sha:
    data["sha"] = sha
# Lähetetään POST-pyyntö tiedoston lisäämiseksi
response = requests.put(api_url, headers=headers, json=data)
print(response.status_code)
print(response.content)