# Machine Learning Model for Bot Detection

## The project
The project’s goal is to make a machine learning model for bot and applications detection. In other words, we want to make a model that can distinguish programmatic traffic from non-programmatic traffic. The dataset is composed by traffic logs collected by a WAAP named Mithril.

### Roadmap:

1. Design the concept of **session** and implement an algorithm capable of grouping http requests into these sessions
2. Identify **meaningful features** to distinguish human from programmatic traffic
3. **Process the dataset** in order to extract the designed features
4. Study the extracted features in order to identify any **correlations** 
5. Choose and implement an **unsupervised machine learning algorithm**
6. Verify and **optimize** the result 


## Table of Content

1. [The Dataset](#the-dataset)
2. [The Concept of Session](#the-concept-of-session)
3. [Features Selection and Design](#features-selection-and-design)
4. [Features Analysis](#features-analysis)
5. [Machine Learning Model](#machine-learning-model)
6. [Results](#results)
7. [To do]()


## The Dataset

Our dataset is composed by <b>traffic logs</b> collected by a WAAP (a sort of firewall), with the following <b>header</b>:
<details> 

<summary>  Expand details : </summary>


* **Timestamp** - The log's timestamp
  - *for example* Mar 24, 2023 @ 17:07:41.000
* **index** - Elastic search index
  - *for example* .ds-waap-logs-2023.03.23-000344
* **customer** - The name of the waap's customer
  - *for example* McDonald
* **Geoip.city_name** - The name of the client's city (ip)
  - *for example* Rome
* **Geoip.continent_name** - The name of the client's continent (ip)
  - *for example* Europe
* **Geoip.country_code2** - The country code of the client (ip)
  - *for example* IT
* **Geoip.country_name** - The country name of the client (ip)
  - *for example* Italy
* **Geoip.region_iso_code** - The iso_code of the client(ip)
  - *for example* IT-RM
* **Geoip.location** - The coordinates of the client (ip)
  - *for example* POINT(12.6843 56.1188)
* **Nodename** - The elasticsearch's node
  - *for example* ip-10-0-4-154.eu-central-1.compute.internal
* **Real_client_ip** - The client's ip
  - *for example* 134.30.168.24
* **service-id** - ID of a customer service
  - *for example* 54fd94af-c2b7-492a-bd6d-617f36bfd0b2

* **transaction.producer.components** - Components of the transaction producer
  - *for example* OWASP_CRS/3.4.0-dev
* **transaction.producer.secrules_engine** - Status of the security rules engine
  - *for example* Enabled
* **transaction.request.body** - Request body content
  - *for example* (empty)
* **transaction.request.headers_json** - Request headers in JSON format, 
  - *for example* {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", "X-Forwarded-Proto": "https", "sec-fetch-site": "same-site", "access-control-request-headers": "authorization,storecode", "accept": "/", "access-control-request-method": "GET", "origin": "blablabla.cloud.customername.it", "sec-fetch-mode": "cors", "X-Amzn-Trace-Id": "Root=1-641dcacd-65d99e7800477fab69c2742e", "Host": "blablablabla.cloud.customername.it", "X-Forwarded-Port": "443", "referer": "blablabla.cloud.customername.it/", "X-Forwarded-For": "44.243.254.234", "sec-fetch-dest": "empty", "accept-encoding": "gzip, deflate, br", "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"}
* **transaction.request.headers_map.content-lenght** - Content length of the request headers map
  - *for example*: 593
* **transaction.request.headers_map_content-type** - Content type of the request headers map
  - *for example*: application/json
* **transaction.request.headers_map.host** - Host in the request headers
  - *for example*: blablabla.cloud.customer.it
* **transaction.request.headers_map.origin** - Origin in the request headers
  - *for example* -
* **transaction.request.headers_map.referer** - Referer in the request headers map
  - *for example* -
* **transaction.request.headers_map.user-agent** - User agent in the request headers
  -  *for example* Amazon-Route53-Health-Check-Service (ref 293dce71-3b67-498f-bd2c-4564e152a418; report amzn.to/1vsLAci)
* **transaction.request.headers_map.x-forwarded-for** - X-Forwarded-For in the request headers map
  - *for example* 44.253.252.234
* **transaction.request.headers_map.x-forwarded-port** - X-Forwarded-Port in the request headers map
  - *for example* 443
* **transaction.request.headers_map.x-forwarded-proto** - X-Forwarded-Proto in the request headers map
  - *for example* https
* **transaction.request.http_version** - HTTP version of the request
  - *for example* 1.1
* **transaction.request.method** - HTTP method of the request
  - *for example* GET
* **transaction.request.uri** - URI of the request
  - *for example* /v1/craftsmen?storeCode=001
* **transaction.request.uri_path** - Path of the URI in the request
  - *for example* /v1/craftsmen
* **transaction.response.body** - Response body content
  - *for example* (empty)
* **transaction.reponse.headers_json** - Response headers in JSON format, 
  - *for example* {"X-waap-Webapp-Group": "pub", "X-waap-Upstream-Latency": "5", "ETag": "W/\"2-vyGp6PvFi4sFtPoIWeDReyIC8\"", "Connection": "keep-alive", "X-Powered-By": "Express", "Content-Type": "application/json; charset=utf-8", "Content-Length": "2", "Date": "Fri, 24 Mar 2023 16:07:41 GMT", "X-waap-Proxy-Latency": "4", "Server": ""}
* **transactin.response.headers_map.content-encoding** - Content encoding in the response headers map
  - *for example* gzip
* **transaction.response.headers_map.content-lenght** - Content length in the response headers map
  - *for example* 96
* **transaction.response.headers_map.content-type** - Content type in the response headers map
  - *for example* application/json
* **transaction.response.headers_map.set-cookie** - Set-Cookie in the response headers map
  - *for example* -
* **transaction.response.headers_map.x-waap-cache** - X-waap-cache in the response headers map
  - *for example* hit
* **transaction.response.headers_map.x-waap-cache-key** - X-waap-cache-key in the response headers map
  - *for example* 6268d5b311ca5w45c2d5306d1f3f22f4
* **transaction.response.headers_map.x-waap-cache-type** - X-waap-cache-type in the response headers map
  - *for example* fresh
* **transaction.response.headers_map.x-waap-proxy-latency** - X-waap-proxy-latency in the response headers map
  - *for example* 34
* **transaction.response.headers_map.x-waap-response-latency** - X-waap-response-latency in the response headers map
  - *for example* 30
* **transaction.response.headers_map.x-waap-upstream-latency** - X-waap-upstream-latency in the response headers map
  - *for example* 966
* **transaction.response.headers.map.x-waap-webapp-group** - X-waap-webapp-group in the response headers map
  - *for example* pub
* **transaction.response.http_code** - HTTP status code of the response
  - *for example* 404
* **transaction.time_stamp** - Timestamp of the transaction
  - *for example* Fri Mar 24 17:07:38 2023
* **transaction.useragent.device** - Device information from the user agent
  - *for example* Other
* **transaction.useragent.family** - User agent family
  - *for example* Amazon-Route53-Health-Check-Service
* **transaction.useragent.os** - Operating system information from the user agent
  - *for example* Other
* **transaction.useragent.os_version** - Operating system version from the user agent
  - *for example* -
* **transaction.useragent.ua_string** - User agent string
  - *for example* Amazon-Route53-Health-Check-Service (ref 293dce71-3b67-498f-bd2c-4564e152a418; report amzn.to/1veLAci)
</details> 

## The Concept of Session
The unit to be distinguished in the model is the unit of a visit to the **same site** by the **same cookie** with the **same user agent** and **IP**. 

Site visits should be defined in terms of **sessions**. The session starts from the **first view** of the cookie page, and page views **within 30 minutes of the previous one** are considered to be the same session. 

If a page view lasts **more than 30 minutes (T),** it is treated as a separate **session**.

### Tweak
Usually, a 30-min period is adopted as the threshold in Web-mining studies. Nevertheless, in my experiments I noticed that using the 30-minute threshold as the only criterion for breaking the click-stream into sessions was not sufficient. I observed the sessions extracted when using the 30-minute value and noticed that, for longer sessions (in terms of number of requests), click-streams belonging to a semantically continuous navigation activity were split into separate sessions. To cope with this issue, I introduce a procedure which adapts the threshold value dynamically, according to the number of session requests so far. In particular, for sessions with less than **rmax** requests so far, I set the threshold value to **t1**. When the number of requests reaches rmax, I increase the threshold value to **t2 > t1**. In other words, we allow a bigger time-lapse between consecutive requests for larger sessions. By trying various threshold values and studying the resulted sessions, we determined that setting **rmax to 100**, **t1 to 30 min** and **t2 to 60 min** gave the best results. 


## Features Selection and Design
A total of <b>19 features</b> was been designed and extracted from our datased:
<details> 

<summary>  Expand details : </summary>

  * **userAgent**: The user agent of the user who made the request.
    - I adopted the **bag of words expression**, a general conversion process of text information
      ```
      Initial State：
      Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1
      Safari/605.1.15

      Transformed：
      mozilla / macintosh / intel / mac / os / x / applewebkit / khtml / like / gecko / version / safari
      ```
  * **noRequests**: The total number of requests (session lenght)
    - This value is obtained by counting the number of requests that compose the session
  
  * **volume**: The total volume of data sent to the client [KB]
    - This value is obtained by summing the volume transferred to the client in each request for each session
  
  * **avgVolume**: The average volume transferred to the client
  
  * **stDevVolume**: The standard deviation of the volume transferred to the client
  
  * **totalTime**: The session duration in seconds
    - This value is obtained by subtracting the timestamp of the most recent request from the least recent one
  
  * **avgTime**: The average time between requests
  
  * **stDevTime**: The standard deviation of the volume transferred to the client between requests
  
  * **Night**: The % of requests made between 2am to 6am (local time)
    - This value was obtained by a conversion of the timezone
  
  * **Repeated**: The reoccurence rate of file requests
  
  * **Error**: The % of requests with status >= 400
  
  * **GET**: The % of requests made with GET method
  
  * **POST**: The % of requests made with POST method
  
  * **OTHER**: The % of requests made with other methods
  
  * **Width**: The width of the traversal path in the url space
  * **Depth**: The depth of the traversal path in the url space
    - The **width and depth** attributes are computed by one string a representative graph based on the URI names of the requested pages. For example, if a session contains requests for the following pages, {/A, /A/B, /A/B/C}, then its width will be 1 and its depth will be 3. Basically, the width attribute measures the number of leaf nodes generated in the graph while the depth attribute measures the maximum depth of the tree(s) within the graph. Therefore, a session that contains requests for {/A, /A/B, /C, /D} will have a width of 3 and a depth of 2.
  
  * **nullReferrer**: The % of requests with referrer = "-"
  
  * **Image**: The % of images requested
  
  * **MaxSustainedClickRate**: The maximum number of clicks in a sliding window.
    - A **click** is a request for an HTML file. This feature corresponds to the maximum number of HTML requests achieved within a certain time-window inside a session. The intuition behind this is that there is an upper bound on the maximum number of clicks that a human can issue within some specific time-frame t, which is dictated by human factors. To capture this feature, we first set the time-frame value of t and then use a sliding window of time t over a given session in order to measure the maximum sustained click rate in that session. For example, if we set t to 12 s and find that the maximum number of clicks within some 12-s time-window inside that session is 36, we conclude that the maximum sustained click rate is 3 clicks per second. This indicates a robot-like rather than a human-like behavior. The sliding window approach starts from the first HTML request of a session and keeps a record of the maximum number of clicks within each window, sliding the window by one HTML request until we reach the last one of the given session. The maximum of all the clicks per window gives the value of this feature
</details> 

## Features Analysis
These are plots of some interesting relationships between the feaures
<details> 

<summary>  Expand details : </summary>
  
  * Distribution between **volume** and **number of requests**
    <center><img src="/img/volume-noreq.png" alt="volume vs number of requests"></center>
  
  * Distribution between **total_time** and **number of requests**
    <center><img src="/img/total_time-noreq.png" alt="total time vs number of requests"></center>
  
  * Distribution between **recurrence** and **number of requests**
    <center><img src="/img/recu-noreq.png" alt="recurrence vs number of requests"></center>
  
  * Distribution between **avgTime** and **total_time**
    <center><img src="/img/avgtime-totaltime.png" alt="average time vs total time"></center>
  
</details>

## Machine Learning Model

The **Kmeans clustering** method was my solution for this unsupervised learning problem. The number of clusters was chosen with a combination of the **elbow method**, **silhouette score** and **domain knowledge,** and finally a total number of **12 clusters** was chosen.

* Elbow Method:
 <center><img src="/img/Elbow.png" alt="elbow method"></center>
 
* Silhouette Score:
 <center><img src="/img/Silhouette.png" alt="Silhouette Score"></center>
 
## Results
The results were explored manually, comparing user agents within the same clusters and the average distance from their centroid

### Cluster 0:
Cluster 0 represents sessions from Facebook mobile applications, we can label this cluster as **Human Traffic**
<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : mozilla / applewebkit / khtml / gecko / mobile / fban / fbios / fbav / fbbv / fbdv / fbmd / fbsn / fbsv / fbss / fbid / phone / fblc / qaau / fbop / fbrv

  - **Media Distanza** : 150.39

  - **Conteggio totale** : 1



* **User Agent** : mozilla / applewebkit / khtml / gecko / mobile / fban / fbios / fbdv / fbmd / fbsn / fbsv / fbss / fbid / phone / fblc / fbop

  - **Media Distanza** : 104.39

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / build / huaweimed / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / fban / fblc / fbav / fbdm / displaymetrics / density / width / height / scaleddensity / xdpi / ydpi / densitydpi / noncompatwidthpixels / noncompatheightpixels / noncompatdensity / noncompatdensitydpi / noncompatxdpi / noncompatydpi

  - **Media Distanza** : 291.64

  - **Conteggio totale** : 1
</details>
#to do

