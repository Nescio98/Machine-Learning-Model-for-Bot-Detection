import pandas as pd
from datetime import datetime
import json
import re

# leggi il dataframe dal file o da una fonte dati
df = pd.read_csv("mydata_new.csv", header=0) #nrows=1000
df = df.drop(columns=["customer"])

# converte la colonna "@timestamp" in un oggetto datetime
#df["@timestamp"] = pd.to_datetime(df["@timestamp"])

# creo nuove colonne
df["volume"] = 0
df["referer"] = "-"
df["image"] = 0
df["css"] = 0
df["js"] = 0
#df["pdf-ps"] = 0
#df["robot.txt"] = False
#df["user-agent"] = ""

def user_agent_to_bag_of_words(user_agent):
    # Rimuovi i numeri, i caratteri speciali e sostituisci gli spazi con '/'
    user_agent = re.sub(r'_|[^\w\s-]|\bref\s+\S+|\breport\s+\S+', ' ', user_agent).replace(' ', '/') #[0-9]+|
    user_agent = re.sub(r'(?<!\w)\d+', '', user_agent).replace('-', " / ")
    #user_agent = re.sub(r'[\w]+(-[\w]+)+', ' ', user_agent).replace(' ', '/')
    

    # Dividi l'user agent in parole
    words = user_agent.split('/')

    # Rimuovi le parole vuote e ripetute
    words = list(filter(lambda x: x != '' and words.count(x) == 1, words))

    # Restituisci le parole rimanenti
    return (' / '.join(words)).lower()

#itero per ogni riga del dataset
for index, row in df.iterrows():

    request_header = json.loads(row["transaction.request.headers_json"])
    response_header = json.loads(row["transaction.response.headers_json"])

    # User Agent
    df.at[index, "transaction.request.headers_map.user-agent"] = user_agent_to_bag_of_words(row["transaction.request.headers_map.user-agent"])

    # Volume
    volume = 0
    if ("Content-Length" in request_header and request_header["Content-Length"] != ""):
        volume += int(request_header["Content-Length"])    
    if ("Content-Length" in response_header and response_header["Content-Length"] != ""):
        volume += int(response_header["Content-Length"])
    df.at[index, "volume"] = volume

    # Referer
    if ("referer" in request_header):
        referer = request_header["referer"]
    else : referer = "-"
    df.at[index, "referer"] = referer

    # Image
    if "Content-Type" in response_header:
        content_type = response_header["Content-Type"]
        if content_type.startswith("image/"): df.at[index, "image"] = 1
        else: df.at[index, "image"] = 0

    # Css
    if "Content-Type" in response_header:
        content_type = response_header["Content-Type"]
        if content_type == "text/css": df.at[index, "css"] = 1
        else: df.at[index, "css"] = 0

    # Js
    if "Content-Type" in response_header:
        content_type = response_header["Content-Type"]
        if content_type == "application/javascript": df.at[index, "js"] = 1
        else: df.at[index, "js"] = 0

    # Robot.txt
    #if "robot.txt" in df["transaction.request.uri_path"]: df.at[index, "robot.txt"] = True

    # Pdf-ps
    #if ".pdf" in df["transaction.request.uri_path"] or ".PDF" in df["transaction.request.uri_path"] or ".ps" in df["transaction.request.uri_path"] or ".eps" in df["transaction.request.uri_path"]: df.at[index, "pdf-ps"] = 1

df = df.rename(columns={
    "transaction.request.headers_map.user-agent": "user-agent",
    "geoip.region_iso_code": "night",
})

df.to_csv("processed_data.csv", index=False)
