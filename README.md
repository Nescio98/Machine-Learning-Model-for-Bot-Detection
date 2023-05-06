# Machine Learning Model for Bot Detection

## The project
The project’s goal is to make a machine learning model for bot and applications detection. In other words, we want to make a model that can distinguish programmatic traffic from non-programmatic traffic. Our dataset are traffic logs collected by a WAAP (a sort of firewall). 

### Roadmap:

1- Identify sessions from our logs by an algorithm that evaluates things like temporal proximity, ip of the client, user agent, cookie.

2- Evaluate the goodness of the algorithm through graphs and data.

3- create a dataset of surely programmatic sessions (e.g., user-agent curl, java, python etc.)

4- Train and evaluate the goodness of the model.

Further developments:

1- Identify possible groups of programmatic sessions (e.g., bots that exfiltrate data, by bots that make attempts at XSS attacks, SQL Injection, by bots that make DDOS attacks, by bots like Googlebot)

2- Grouping programmatic sessions and finding the semantics of the groups found

## The Dataset
Our dataset is composed by **traffic logs** collected by a WAAP (a sort of firewall), with the following *header* :
* **Timestamp** - The log's timestamp, *for example* Mar 24, 2023 @ 17:07:41.000
* **index** - Elastic search index, *for example* .ds-waap-logs-2023.03.23-000344
* **customer** - The name of the waap's customer, *for example* McDonald
* **Geoip.city_name** - The name of the client's city (ip), *for example* Rome
* **Geoip.continent_name** - The name of the client's continent (ip), *for example* Europe
* **Geoip.country_code2** - The country code of the client (ip), *for example* IT
* **Geoip.country_name** - The country name of the client (ip), *for example* Italy
* **Geoip.region_iso_code** - The iso_code of the client(ip), *for example* IT-RM
* **Geoip.location** - The coordinates of the client (ip), *for example* POINT(12.6843 56.1188)
* **Nodename** - The elasticsearch's node, *for example* ip-10-0-4-154.eu-central-1.compute.internal
* **Real_client_ip** - The client's ip, *for example* 134.30.168.24
* Rules - Rule raised by the WAAP
* service-id - ID of a customer service, *for example* 54fd94af-c2b7-492a-bd6d-617f36bfd0b2

#to do
