import pandas as pd
from datetime import datetime
import json
import re


# Read the dataframe from the file or from a data source
df = pd.read_csv("mydata.csv", header=0) #nrows=1000
df = df.drop(columns=["customer"])


# creo nuove colonne
df["volume"] = 0
df["referer"] = "-"
df["image"] = 0
df["css"] = 0
df["js"] = 0


def user_agent_to_bag_of_words(user_agent):
    """
    Convert the user agent string to a bag of words representation.

    Args:
        user_agent (str): User agent string.

    Returns:
        str: Bag of words representation of the user agent.
    """
    # Remove numbers, special characters, and replace spaces with '/'
    user_agent = re.sub(r'[0-9]+|_|[^\w\s-]|\bref\s+\S+|\breport\s+\S+', ' ', user_agent).replace(' ', '/') #[0-9]+|
    user_agent = re.sub(r'(?<!\w)\d+', '', user_agent).replace('-', "/")

    # Split the user agent into words
    words = user_agent.split('/')

    # Remove empty and repeated words.
    words = list(filter(lambda x: x != '' and words.count(x) == 1 and x != ' ' and len(x)>3, words))

    # Return the remaining words
    return (' / '.join(words)).lower()

# Iter for each row of the dataset
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
    if ("referer" in request_header) and request_header["referer"] != "":
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

df = df.rename(columns={
    "transaction.request.headers_map.user-agent": "user-agent",
    "geoip.region_iso_code": "night",
})

df.to_csv("processed_data_new.csv", index=False)
