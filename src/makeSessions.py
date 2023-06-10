import pandas as pd
import utility
import numpy as np
from datetime import timedelta
from dateutil.parser import parse

# Read the dataframe from a file or data source
df = pd.read_csv("processed_data_new.csv", header=0) # nrows=1000

# Convert the "@timestamp" column to a datetime object
df["@timestamp"] = pd.to_datetime(df["@timestamp"])

# Create new columns "session_id", "noRequests" with initial values
df["session_id"] = ""
df["noRequests"] = 1

# Initialization of some columns
df["avgTime"] = df["@timestamp"]
df["stDevTime"] = df["@timestamp"]
df["avgVolume"] = df["volume"]
df["stDevVolume"] = df["volume"]
df["maxSustainedClickRate"] = df["@timestamp"]
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

session_hashmap = {}  # {session: [id, timestamp, total_requests]}
current_session_id = 0

for index, row in df.iterrows():
    hashmap_key = str(row["real_client_ip"]) + str(row["service-id"])  # hashmap_key = ip+service_id
    if (hashmap_key in session_hashmap) and (
        (row["@timestamp"] - session_hashmap[hashmap_key][1]) <= pd.Timedelta(
            "30 minutes" if session_hashmap[hashmap_key][2] < 100 else "60 minutes"
        )
    ):
        session_id = session_hashmap[hashmap_key][0]  # session_id
        df.at[index, "session_id"] = session_id
        number_of_requests = session_hashmap[hashmap_key][2] + 1  # number of request per session
        session_hashmap[hashmap_key] = [session_id, row["@timestamp"], number_of_requests]
    else:
        current_session_id += 1
        session_hashmap[str(row["real_client_ip"]) + str(row["service-id"])] = [
            current_session_id,
            row["@timestamp"],
            0,
        ]
        df.at[index, "session_id"] = current_session_id


def total_time(x):
    """Calculate the total time in seconds for each session."""
    result = x.max() - x.min()
    return result.total_seconds()


def average_time(x):
    """Calculate the average time between page requests."""
    if len(x) > 1:
        difference = [(x.iloc[i] - x.iloc[i - 1]).total_seconds() for i in range(1, len(x))]
        mean = np.mean(difference)
        return mean
    return 0


def stdDev_time(x):
    """Calculate the standard deviation of time between page requests."""
    if len(x) > 2:
        difference = [(x.iloc[i] - x.iloc[i - 1]).total_seconds() for i in range(1, len(x))]
        standard_dev = np.std(difference)
        return standard_dev
    return 0


def average_volume(x):
    """Calculate the average volume between requests."""
    if len(x) > 1:
        volume = [x.iloc[i] for i in range(0, len(x))]
        mean = np.mean(volume)
        return mean
    return 0


def stdDev_volume(x):
    """Calculate the standard deviation of volume between requests."""
    if len(x) > 2:
        volume = [x.iloc[i] for i in range(0, len(x))]
        standard_dev = np.std(volume)
        return standard_dev
    return 0


def recurrence(x):
    """Calculate the recurrence rate of requested files."""
    n = len(x)
    repetitions = n - len(set(x))
    return (repetitions / n)


def errors(x):
    """Calculate the errors rate."""
    greater_than_400 = [1 for i in range(0, len(x)) if x.iloc[i] >= 400]
    return sum(greater_than_400) / len(x)


def get(x):
    """Calculate the GET rate."""
    list_of_gets = [1 for i in range(0, len(x)) if x.iloc[i] == "GET"]
    return sum(list_of_gets) / len(x)


def post(x):
    """Calculate the POST rate."""
    list_of_posts = [1 for i in range(0, len(x)) if x.iloc[i] == "POST"]
    return sum(list_of_posts) / len(x)


def head(x):
    """Calculate the HEAD rate."""
    list_of_heads = [1 for i in range(0, len(x)) if x.iloc[i] == "HEAD"]
    return sum(list_of_heads) / len(x)


def other(x):
    """Calculate the rate for methods other than HEAD, GET, and POST."""
    list_of_others = [
        1 for i in range(0, len(x)) if x.iloc[i] != "HEAD" and x.iloc[i] != "GET" and x.iloc[i] != "POST"
    ]
    return sum(list_of_others) / len(x)


def nullRef(x):
    """Calculate the null referer rate."""
    list_of_nullRef = [1 for i in range(0, len(x)) if x.iloc[i] == "-"]
    return sum(list_of_nullRef) / len(x)


def image_rate(x):
    """Calculate the rate of requests for images."""
    list_of_image = [1 for i in range(0, len(x)) if x.iloc[i] == 1]
    return sum(list_of_image) / len(x)


def css_rate(x):
    """Calculate the rate of requests for CSS."""
    list_of_css = [1 for i in range(0, len(x)) if x.iloc[i] == 1]
    return sum(list_of_css) / len(x)


def js_rate(x):
    """Calculate the rate of requests for JavaScript."""
    list_of_js = [1 for i in range(0, len(x)) if x.iloc[i] == 1]
    return sum(list_of_js) / len(x)


def width_url(x):
    """Calculate the width of the URL."""
    width = 0
    width_list = []
    for url in x:
        path_components = url.strip("/").split("/")
        if path_components[0] not in width_list:
            width_list.append(path_components[0])
            width += 1
    return width


def depth_url(x):
    """Calculate the depth of the URL."""
    depth = 0
    nodes = {}
    for url in x:
        path_components = url.strip("/").split("/")
        current_node = nodes
        for component in path_components:
            if component not in current_node:
                current_node[component] = {}
            current_node = current_node[component]
        depth = max(depth, len(path_components))
    return depth


def night(x):
    """Calculate the rate of requests during the night (2 AM - 7 AM)."""
    hashmap = utility.hashmap_timezone
    res = 0
    for i in range(0, len(x)):
        dt, iso_region = x.iloc[i].split("/")
        dt = parse(dt)
        if iso_region != "-":
            if iso_region in hashmap:
                operation, minutes = hashmap[iso_region].split("UTC")[1].split(":")
                hours = operation[1:]
                operation = operation[0]
                delta = timedelta(hours=int(hours), minutes=int(minutes))
                if operation == "+":
                    dt = dt + delta
                else:
                    dt = dt - delta
            else:
                substring = iso_region.split("-")[0] + "-"
                operation, minutes = hashmap[substring].split("UTC")[1].split(":")
                hours = operation[1:]
                operation = operation[0]
                delta = timedelta(hours=int(hours), minutes=int(minutes))
                if operation == "+":
                    dt = dt + delta
                else:
                    dt = dt - delta
        if dt.hour >= 2 and dt.hour < 7:
            res += 1
    return (res / len(x))


# Group the dataframe by "session_id" and aggregate the columns of interest
grouped_df = df.groupby("session_id").agg(
    {
        "user-agent": "first",
        "noRequests": "sum",
        "volume": "sum",
        "@timestamp": total_time,
        "avgTime": average_time,
        "stDevTime": stdDev_time,
        "avgVolume": average_volume,
        "stDevVolume": stdDev_volume,
        "recurrence": recurrence,
        "errors": errors,
        "get": get,
        "post": post,
        "head": head,
        "others": other,
        "nullReferer": nullRef,
        "image": image_rate,
        "css": css_rate,
        "js": js_rate,
        "width": width_url,
        "depth": depth_url,
        "night": night,
    }
)

# Rename the columns for clarity
grouped_df = grouped_df.rename(
    columns={
        "@timestamp": "total_time",
    }
)

# Save the aggregated dataframe to a new file or data source
grouped_df.to_csv("sessions_new.csv", index=False)
