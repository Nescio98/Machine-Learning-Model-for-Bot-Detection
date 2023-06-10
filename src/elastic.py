import csv
from elasticsearch import Elasticsearch
import utility


def process_hits(hits):
    """
    Process the hits returned by Elasticsearch and write them to a CSV file.

    Args:
        hits (list): List of hits returned by Elasticsearch.

    Returns:
        None
    """
    with open('mydata_new.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        data = []
        for hit in range(len(hits)):
            for field in fields:
                if field in hits[hit]['fields']:
                    data.append(hits[hit]['fields'][field][0])
                else:
                    data.append("-")
            writer.writerow(data)
            data.clear()


# Elasticsearch configuration
password = utility.password
username = utility.username
index = utility.index

# Fields to fetch from Elasticsearch
fields = ["@timestamp", "customer", "geoip.region_iso_code", "real_client_ip", "service-id",
          "transaction.request.headers_json", "transaction.request.method", "transaction.request.uri_path",
          "transaction.response.headers_json", "transaction.response.http_code",
          "transaction.request.headers_map.user-agent"]

# Create CSV file and write the header row
with open('mydata_new.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

# Create Elasticsearch client
es = Elasticsearch(['https://mithril.' + index], basic_auth=(username, password), request_timeout=30,
                   verify_certs=False)

# Search and scroll through the data
data = es.search(index=index, size=10000, fields=fields,
                 query={"range": {"@timestamp": {"format": "strict_date_optional_time",
                                                 "gte": "2023-05-02T10:00:00.955Z",
                                                 "lte": "2023-05-02T12:30:00.955Z"}}},
                 sort={"@timestamp": {"order": "asc"}}, scroll="2m")

print(len(data['hits']['hits']))  # number of docs

sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])

while scroll_size > 0:
    # "Scrolling..."

    # Before scroll, process current batch of hits
    process_hits(data['hits']['hits'])

    data = es.scroll(scroll_id=sid, scroll='2m')

    # Update the scroll ID
    sid = data['_scroll_id']

    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])

# Clear the scroll
es.clear_scroll(scroll_id=sid)

    