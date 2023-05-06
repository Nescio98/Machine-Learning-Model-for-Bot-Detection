import pandas as pd
import utility
import numpy as np
from datetime import timedelta
from dateutil.parser import parse

# leggi il dataframe dal file o da una fonte dati
df = pd.read_csv("processed_data.csv", header=0) # nrows=1000

# converte la colonna "@timestamp" in un oggetto datetime
df["@timestamp"] = pd.to_datetime(df["@timestamp"])

# ordina il dataframe per "@timestamp"
#df = df.sort_values(by="@timestamp")

# crea una nuova colonna "session_id"
df["session_id"] = ""
df["noRequests"] = 1

#da spostare in dataprocess.py
#df = df.drop(columns=["customer"])
df["avgTime"] = df["@timestamp"]
df["stDevTime"] = df["@timestamp"]
#df["maxSustainedClickRate"] = df["@timestamp"]
df["recurrence"] = df["transaction.request.uri_path"]
df["errors"] = df["transaction.response.http_code"]
df["get"] = df["transaction.request.method"]
df["post"] = df["transaction.request.method"]
df["head"] = df["transaction.request.method"]
df["others"] = df["transaction.request.method"]
df["nullReferer"] = df["referer"]
df["width"] = df["transaction.request.uri_path"]
df["depth"] = df["transaction.request.uri_path"]
df["night"] = df["@timestamp"].apply(str) + "/" + df["night"].apply(str)


session_hashmap = {}#{session:[id,timestamp,total_requests]}



current_session_id = 0
for index, row in df.iterrows():
    hashmap_key = str(row["real_client_ip"]) + str(row["user-agent"]) + str(row["service-id"]) # hashmap_key = ip+user_agent+service_id
    if (hashmap_key in session_hashmap): 
        treshold = "30 minutes" if session_hashmap[hashmap_key][2] < 100 else "60 minutes"
        #if treshold == "60 minutes":print(treshold)
    if (hashmap_key in session_hashmap) and ((row["@timestamp"] - session_hashmap[hashmap_key][1]) <= pd.Timedelta("30 minutes" if session_hashmap[hashmap_key][2] < 100 else "60 minutes")):
        session_id =  session_hashmap[hashmap_key][0] #session_id
        df.at[index, "session_id"] = session_id
        number_of_requests = session_hashmap[hashmap_key][2] + 1 #number of request per session
        session_hashmap[hashmap_key] = [current_session_id,row["@timestamp"],number_of_requests]
    else:
        current_session_id += 1
        session_hashmap[str(row["real_client_ip"]) + str(row["user-agent"]) + str(row["service-id"])] = [current_session_id,row["@timestamp"],0]
        df.at[index, "session_id"] = current_session_id

#total time in seconds for each session
def total_time(x):
    result = x.max() - x.min()
    return result.total_seconds()

#average time between page request
def average_time(x):
    if len(x)> 1 :
        # Utilizziamo una list comprehension per calcolare le differenze tra i valori adiacenti
        difference = [(x.iloc[i] - x.iloc[i-1]).total_seconds() for i in range(1, len(x))]
        mean = np.mean(difference)
        return mean

    return 0

def stdDev_time(x):
    if len(x)> 2 :
        # Utilizziamo una list comprehension per calcolare le differenze tra i valori adiacenti
        difference = [(x.iloc[i] - x.iloc[i-1]).total_seconds() for i in range(1, len(x))]
        standard_dev = np.std([diff for diff in difference])
        return standard_dev
    return 0

# recurrence rate of file requested rate= repeated files / total files
def recurrence(x):
    n = len(x)
    repetitions = n - len(set(x))
    return (repetitions / n)

# errors rate
def errors(x):
    greater_than_400 = [1 for i in range(0,len(x)) if x.iloc[i] >= 400]
    return sum(greater_than_400) / len(x)

# get rate
def get(x):
    list_of_gets = [1 for i in range(0,len(x)) if x.iloc[i] == "GET"]
    return sum(list_of_gets) / len(x)

# post rate
def post(x):
    list_of_posts = [1 for i in range(0,len(x)) if x.iloc[i] == "POST"]
    return sum(list_of_posts) / len(x)

# head rate
def head(x):
    list_of_heads = [1 for i in range(0,len(x)) if x.iloc[i] == "HEAD"]
    return sum(list_of_heads) / len(x)

# others rate
def other(x):
    list_of_others = [1 for i in range(0,len(x)) if x.iloc[i] != "HEAD" and  x.iloc[i] != "GET" and  x.iloc[i] != "POST"]
    return sum(list_of_others) / len(x)

# null referer rate
def nullRef(x):
    list_of_nullRef = [1 for i in range(0,len(x)) if x.iloc[i] == "-"]
    return sum(list_of_nullRef) / len(x)

def image_rate(x):
    list_of_image = [1 for i in range(0,len(x)) if x.iloc[i] == 1]
    return sum(list_of_image) / len(x)

def css_rate(x):
    list_of_css = [1 for i in range(0,len(x)) if x.iloc[i] == 1]
    return sum(list_of_css) / len(x)

def js_rate(x):
    list_of_js = [1 for i in range(0,len(x)) if x.iloc[i] == 1]
    return sum(list_of_js) / len(x)

def width_url(x):
    # initialize the width  0
    width = 0          
    width_list = []    
    # iterate over each URL in the list
    for url in x:
        # split the URL into its path components
        path_components = url.strip("/").split("/")
        if (path_components[0] not in width_list):
          width_list.append(path_components[0])
          width += 1   
    # return the width 
    return width

def depth_url(x):
    # initialize  depth to 0
    depth = 0    
    # create an empty dictionary to store the nodes and their children
    nodes = {}    
    # iterate over each URL in the list
    for url in x:
        # split the URL into its path components
        path_components = url.strip("/").split("/")        
        # initialize the current node to the root
        current_node = nodes        
        # iterate over each path component
        for component in path_components:
            # if the component is not in the current node's children, add it
            if component not in current_node:
                current_node[component] = {}            
            # move down to the child node
            current_node = current_node[component]       
        # update the depth if necessary
        depth = max(depth, len(path_components))    
    # return the width and depth
    return depth

def night(x):
    hashmap = utility.hashmap_timezone
    res = 0
    for i in range(0,len(x)):
        dt,iso_region = x.iloc[i].split("/")
        dt = parse(dt)
        if iso_region != "-":
            if iso_region in hashmap:
                operation, minutes = hashmap[iso_region].split("UTC")[1].split(":")
                hours = operation[1:]
                operation = operation[0]
                delta = timedelta(hours=int(hours), minutes=int(minutes))
                if operation == "+":
                    dt = dt + delta
                else : dt = dt - delta
            else: 
                substring = iso_region.split('-')[0] + '-'
                operation, minutes = hashmap[substring].split("UTC")[1].split(":")
                hours = operation[1:]
                operation = operation[0]
                delta = timedelta(hours=int(hours), minutes=int(minutes))
                if operation == "+":
                    dt = dt + delta
                else : dt = dt - delta   
        if dt.hour >= 2 and dt.hour < 7:
            res += 1         
    return (res / len(x))





# raggruppa il dataframe per "session_id" e aggrega le colonne di interesse
grouped_df = df.groupby("session_id").agg({
    "user-agent" : "first",
    "noRequests": "sum",
    "volume" : "sum",
    "@timestamp" : total_time,
    "avgTime" : average_time,
    "stDevTime" : stdDev_time,
    "recurrence" : recurrence,
    "errors" : errors,
    "get" : get,
    "post" : post,
    "head" : head,
    "others" : other,
    "nullReferer" : nullRef,
    "image": image_rate,
    "css": css_rate,
    "js" : js_rate,
    "width" : width_url,
    "depth" : depth_url,
    "night" : night,
})

# rinomina le colonne per chiarezza
grouped_df = grouped_df.rename(columns={
    "@timestamp": "total_time",
})

# salva il dataframe aggregato in un nuovo file o in una fonte dati
grouped_df.to_csv("sessions_new.csv", index=False)
