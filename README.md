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
7. [References](#references)


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


### Cluster 1:
Cluster 1 represents sessions from applications such as python, java, and other bots, so we can label this as **Programmatic Traffic**
<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : apache / httpclient / java

  - **Media Distanza** : 22.11

  - **Conteggio totale** : 15



* **User Agent** : java / http / client

  - **Media Distanza** : 54.34

  - **Conteggio totale** : 2



* **User Agent** : linkedinbot / compatible / mozilla / apache / httpclient / http / linkedin

  - **Media Distanza** : 122.72

  - **Conteggio totale** : 1



* **User Agent** : mozilla / compatible / msie / windows / trident / slcc / media / center / cmdtdfjs / wbxapp / zoom

  - **Media Distanza** : 216.21

  - **Conteggio totale** : 1



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / chrome / safari / edition / campaign

  - **Media Distanza** : 123.64

  - **Conteggio totale** : 1



* **User Agent** : python / aiohttp

  - **Media Distanza** : 94.96

  - **Conteggio totale** : 1



* **User Agent** : python / requests

  - **Media Distanza** : 56.25

  - **Conteggio totale** : 4



* **User Agent** : zoominfobot / zoominfobot / zoominfo

  - **Media Distanza** : 123.63

  - **Conteggio totale** : 1
  
  </details>
  
### Cluster 2:
Cluster 2 represents sessions from apple mobile devices and we can label this traffic as **Human Traffic**
<details> 

<summary>  Expand details : </summary>
  
* **User Agent**: mozilla / applewebkit / khtml / gecko / crios / mobile / safari
  - **Media Distanza**: 13.66
  - **Conteggio totale**: 42

* **User Agent**: mozilla / applewebkit / khtml / gecko / edgios / version / mobile / safari
  - **Media Distanza**: 62.43
  - **Conteggio totale**: 2

* **User Agent**: mozilla / applewebkit / khtml / gecko / mobile
  - **Media Distanza**: 4.47
  - **Conteggio totale**: 25

* **User Agent**: mozilla / applewebkit / khtml / gecko / mobile / safari
  - **Media Distanza**: 4.30
  - **Conteggio totale**: 43

* **User Agent**: mozilla / applewebkit / khtml / gecko / version / mobile / safari
  - **Media Distanza**: 3.82
  - **Conteggio totale**: 621

* **User Agent**: mozilla / ipad / applewebkit / khtml / gecko / crios / mobile / safari
  - **Media Distanza**: 33.81
  - **Conteggio totale**: 1

* **User Agent**: mozilla / ipad / applewebkit / khtml / gecko / mobile
  - **Media Distanza**: 31.40
  - **Conteggio totale**: 1

* **User Agent**: mozilla / ipad / applewebkit / khtml / gecko / mobile / safari
  - **Media Distanza**: 31.30
  - **Conteggio totale**: 3

* **User Agent**: mozilla / ipad / applewebkit / khtml / gecko / version / mobile / safari
  - **Media Distanza**: 31.15
  - **Conteggio totale**: 3

* **User Agent**: mozilla / macintosh / intel / applewebkit / khtml / like / gecko
  - **Media Distanza**: 7.73
  - **Conteggio totale**: 5

* **User Agent**: mozilla / macintosh / intel / applewebkit / khtml / like / gecko / chrome / safari
  - **Media Distanza**: 7.82
  - **Conteggio totale**: 113

* **User Agent**: mozilla / macintosh / intel / applewebkit / khtml / like / gecko / version / mobile / safari
  - **Media Distanza**: 6.23
  - **Conteggio totale**: 3

* **User Agent**: mozilla / macintosh / intel / applewebkit / khtml / like / gecko / version / safari
  - **Media Distanza**: 6.77
  - **Conteggio totale**: 124

* **User Agent**: mozilla / macintosh / intel / applewebkit / khtml / like / gecko / version / safari / applebot / http / apple / applebot
  - **Media Distanza**: 42.62
  - **Conteggio totale**: 8

* **User Agent**: mozilla / macintosh / intel / gecko / firefox
  - **Media Distanza**: 9.97
  - **Conteggio totale**: 20
  </details>
  
### Cluster 3
Cluster 3 represents sessions from yandexbot and we can label this traffic as **Programmatic Traffic**
<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : mozilla / compatible / yandexbot / http / yandex / bots
  - **Media Distanza** : 5.91
  - **Conteggio totale** : 88

* **User Agent** : mozilla / compatible / yandexbot / http / yandex / bots / applewebkit / khtml / like / gecko / chrome
  - **Media Distanza** : 5.96
  - **Conteggio totale** : 7

* **User Agent** : mozilla / compatible / yandexrenderresourcesbot / http / yandex / bots / applewebkit / khtml / like / gecko / chrome
  - **Media Distanza** : 22.46
  - **Conteggio totale** : 16
</details>

### Cluster 4

Cluster 4 represents sessions from reactor netty and we can label this traffic as **Programmatic Traffic**
<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : reactornetty / release

  - **Media Distanza** : 1.00

  - **Conteggio totale** : 11
 </details>
 
 
### Cluster 5

Cluster 5 represents sessions from differents bots, like GoogleBot, and we can label this traffic as **Programmatic Traffic**
<details> 

<summary>  Expand details : </summary>

**User Agent** : adsbot / google / http / google / adsbot / html
- **Media Distanza** : 31.02
- **Conteggio totale** : 9

**User Agent** : chrome / privacy / preserving / prefetch / proxy
- **Media Distanza** : 78.67
- **Conteggio totale** : 5

**User Agent** : dalvik / linux / android / build
- **Media Distanza** : 51.55
- **Conteggio totale** : 2

**User Agent** : dalvik / linux / android / huawei / build / huaweilyo
- **Media Distanza** : 102.85
- **Conteggio totale** : 1

**User Agent** : expanse / palo / alto / networks / company / searches / across / global / space / multiple / times / identify / customers / presences / internet / would / like / excluded / from / scans / please / send / addresses / domains / scaninfo / paloaltonetworks
- **Media Distanza** : 217.82
- **Conteggio totale** : 4

**User Agent** : facebookexternalhit / http / facebook / externalhit / uatext
- **Media Distanza** : 124.90
- **Conteggio totale** : 2

**User Agent** : googlebot / image
- **Media Distanza** : 33.86
- **Conteggio totale** : 4

**User Agent** : leroy / merlin / leroymerlin / festadelbricolage / build / alamofire
- **Media Distanza** : 9.55
- **Conteggio totale** : 185

**User Agent** : leroy / merlin / leroymerlin / festadelbricolage / build / alamofire / appioslmit
- **Media Distanza** : 21.14
- **Conteggio totale** : 1

**User Agent** : mozilla / applewebkit / khtml / gecko / version / safari / compatible / adsbot / google / http / google / mobile / adsbot / html
- **Media Distanza** : 31.45
- **Conteggio totale** : 1

**User Agent** : mozilla / applewebkit / khtml / like / gecko / compatible / googlebot / http / google / html / chrome / safari
- **Media Distanza** : 13.80
- **Conteggio totale** : 29

**User Agent** : mozilla / compatible / coccocbot / http / help / coccoc / searchengine
- **Media Distanza** : 62.37
- **Conteggio totale** : 3

**User Agent** : mozilla / compatible / coccocbot / image / http / help / coccoc / searchengine
- **Media Distanza** : 69.86
- **Conteggio totale** : 4

**User Agent** : mozilla / compatible / dotbot / https / opensiteexplorer / dotbot / help
- **Media Distanza** : 61.09
- **Conteggio totale** : 5

**User Agent** : mozilla / compatible / googlebot / http / google / html
- **Media Distanza** : 13.51
- **Conteggio totale** : 35

**User Agent** : mozilla / compatible / qwantify / https / qwant
- **Media Distanza** : 125.53
- **Conteggio totale** : 1

**User Agent** : mozilla / compatible / semrushbot / http / semrush / html
- **Media Distanza** : 42.17
- **Conteggio totale** : 9

**User Agent** : mozilla / compatible / seznambot / http / napoveda / seznam / seznambot / intro
- **Media Distanza** : 88.01
- **Conteggio totale** : 4

**User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / chrome / mobile / safari / compatible / google / read / aloud / https / support / google / webmasters / answer
- **Media Distanza** : 62.16
- **Conteggio totale** : 10

**User Agent** : mozilla / linux / android / nexus / build / applewebkit / khtml / like / gecko / chrome / mobile / safari / compatible / googlebot / http / google / html
- **Media Distanza** : 18.52
- **Conteggio totale** : 44

**User Agent** : mozilla / linux / applewebkit / khtml / like / gecko / chrome / safari / pagerenderer / https / developers / google / snippet
- **Media Distanza** : 58.04
- **Conteggio totale** : 7

**User Agent** : mozilla / linux / netcast / applewebkit / khtml / like / gecko / chrome / safari / smarttv / colt
- **Media Distanza** : 152.99
- **Conteggio totale** : 1

**User Agent** : mozilla / windows / skypeuripreview / preview / skype / preview / microsoft
- **Media Distanza** : 159.18
- **Conteggio totale** : 1
  </details>
  
  
### Cluster 6

Cluster 6 represents sessions from differents android mobile devices, and we can label this traffic as **Human Traffic**
<details> 

<summary>  Expand details : </summary>

* **User Agent** : mithril / function / write

  - **Media Distanza** : 153.26

  - **Conteggio totale** : 1



* **User Agent** : mozilla / android / mobile / gecko / firefox

  - **Media Distanza** : 7.84

  - **Conteggio totale** : 14



* **User Agent** : mozilla / android / tablet / gecko / firefox

  - **Media Distanza** : 88.63

  - **Conteggio totale** : 1



* **User Agent** : mozilla / applewebkit / khtml / gecko / fxios / mobile / safari

  - **Media Distanza** : 62.57

  - **Conteggio totale** : 2



* **User Agent** : mozilla / applewebkit / khtml / gecko / mobile / appioslmit / leroy / merlin

  - **Media Distanza** : 19.92

  - **Conteggio totale** : 21



* **User Agent** : mozilla / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 8.52

  - **Conteggio totale** : 1



* **User Agent** : mozilla / applewebkit / khtml / like / gecko / compatible / http / bing / chrome / safari

  - **Media Distanza** : 14.99

  - **Conteggio totale** : 69



* **User Agent** : mozilla / cros / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 39.89

  - **Conteggio totale** : 5



* **User Agent** : mozilla / gecko / firefox

  - **Media Distanza** : 7.77

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 4.05

  - **Conteggio totale** : 924



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / chrome / mobile / safari / edga

  - **Media Distanza** : 28.08

  - **Conteggio totale** : 8



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 3.55

  - **Conteggio totale** : 15



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / chrome / yabrowser / mobile / safari

  - **Media Distanza** : 88.36

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / version / chrome / mobile / duckduckgo / safari

  - **Media Distanza** : 39.91

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / version / chrome / mobile / safari

  - **Media Distanza** : 8.33

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / armor / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 88.39

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / asus / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 51.08

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 7.17

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari

  - **Media Distanza** : 6.57

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / fbav

  - **Media Distanza** : 26.23

  - **Conteggio totale** : 8



* **User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / leroy / merlin / appandroidlmit

  - **Media Distanza** : 9.15

  - **Conteggio totale** : 64



* **User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 17.65

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser / swan / mibrowser

  - **Media Distanza** : 126.13

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / build / huaweiane / applewebkit / khtml / like / gecko / version / chrome / mobile / safari

  - **Media Distanza** : 88.53

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / build / huaweimar / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / leroy / merlin / appandroidlmit

  - **Media Distanza** : 88.77

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / build / huaweipra / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 62.94

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / hmscore / applewebkit / khtml / like / gecko / chrome / huaweibrowser / mobile / safari

  - **Media Distanza** : 72.16

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / hmscore / gmscore / applewebkit / khtml / like / gecko / chrome / huaweibrowser / mobile / safari

  - **Media Distanza** : 95.42

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / huawei / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 13.86

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / kfonwi / applewebkit / khtml / gecko / silk / chrome / safari

  - **Media Distanza** : 124.94

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / lenovo / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 51.06

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / android / lite / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 25.65

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / lite / applewebkit / khtml / like / gecko / chrome / mobile / safari / edga

  - **Media Distanza** : 37.89

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / lite / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 30.98

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / android / midnight / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 88.38

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / moto / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 25.64

  - **Conteggio totale** : 8



* **User Agent** : mozilla / linux / android / moto / build / rons / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 92.06

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / moto / plus / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 44.24

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / moto / power / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 91.95

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / motorola / edge / lite / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 69.37

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / motorola / edge / plus / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 73.92

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / motorola / razr / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 102.01

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / nokia / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 62.53

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / note / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / leroy / merlin / appandroidlmit

  - **Media Distanza** : 14.09

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / note / lite / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 30.18

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / note / lite / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / leroy / merlin / appandroidlmit

  - **Media Distanza** : 29.09

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / note / lite / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 32.80

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / oneplus / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 31.35

  - **Conteggio totale** : 5



* **User Agent** : mozilla / linux / android / oneplus / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari

  - **Media Distanza** : 31.91

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / oneplus / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / leroy / merlin / appandroidlmit

  - **Media Distanza** : 32.60

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / pixel / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 33.49

  - **Conteggio totale** : 6



* **User Agent** : mozilla / linux / android / poco / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 64.89

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / redmi / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 11.08

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / redmi / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 20.71

  - **Conteggio totale** : 4



* **User Agent** : mozilla / linux / android / redmi / note / applewebkit / khtml / like / gecko / chrome / mobile / safari

  - **Media Distanza** : 15.61

  - **Conteggio totale** : 19



* **User Agent** : mozilla / linux / android / redmi / note / applewebkit / khtml / like / gecko / chrome / mobile / safari / edga

  - **Media Distanza** : 31.87

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / redmi / note / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / fbav

  - **Media Distanza** : 30.26

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / redmi / note / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / leroy / merlin / appandroidlmit

  - **Media Distanza** : 17.60

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / redmi / note / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 23.42

  - **Conteggio totale** : 19



* **User Agent** : mozilla / linux / android / redmi / plus / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 41.62

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / samsung / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 7.91

  - **Conteggio totale** : 238



* **User Agent** : mozilla / linux / android / samsung / applewebkit / khtml / like / gecko / samsungbrowser / chrome / safari

  - **Media Distanza** : 7.92

  - **Conteggio totale** : 6



* **User Agent** : mozilla / linux / android / samsung / bxxs / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 62.83

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / samsung / bxxu / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 30.39

  - **Conteggio totale** : 7



* **User Agent** : mozilla / linux / android / samsung / bxxu / ewch / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 93.34

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / samsung / bxxu / hwce / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 93.34

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / samsung / fnxxs / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 51.46

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / android / samsung / fxxsghwc / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 88.67

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / samsung / fxxu / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 88.60

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / samsung / fxxubcsi / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 88.62

  - **Conteggio totale** : 1



* **User Agent** : mozilla / linux / android / samsung / fxxuhfvg / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 62.86

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / samsung / gxxs / applewebkit / khtml / like / gecko / samsungbrowser / chrome / mobile / safari

  - **Media Distanza** : 62.90

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / android / xiaomi / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / xiaomi / miuibrowser

  - **Media Distanza** : 22.20

  - **Conteggio totale** : 3



* **User Agent** : mozilla / linux / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 4.93

  - **Conteggio totale** : 36



* **User Agent** : mozilla / linux / applewebkit / khtml / like / gecko / chrome / safari / xiaomi / miuibrowser

  - **Media Distanza** : 16.89

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / applewebkit / khtml / like / gecko / samsungbrowser / chrome / safari

  - **Media Distanza** : 6.00

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / gecko / firefox

  - **Media Distanza** : 7.72

  - **Conteggio totale** : 5



* **User Agent** : mozilla / smart / linux / tizen / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 124.96

  - **Conteggio totale** : 1



* **User Agent** : mozilla / ubuntu / linux / gecko / firefox

  - **Media Distanza** : 37.18

  - **Conteggio totale** : 6



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / chrome / safari

  - **Media Distanza** : 4.26

  - **Conteggio totale** : 1771



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / chrome / safari / atcontent

  - **Media Distanza** : 88.39

  - **Conteggio totale** : 1



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / chrome / safari / edge

  - **Media Distanza** : 40.44

  - **Conteggio totale** : 2



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / chrome / safari / trailer

  - **Media Distanza** : 88.36

  - **Conteggio totale** : 1



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / chrome / safari / unique

  - **Media Distanza** : 88.37

  - **Conteggio totale** : 1



* **User Agent** : mozilla / windows / applewebkit / khtml / like / gecko / compatible / ezndno / chrome / safari

  - **Media Distanza** : 51.32

  - **Conteggio totale** : 3



* **User Agent** : mozilla / windows / gecko / firefox

  - **Media Distanza** : 7.87

  - **Conteggio totale** : 185



* **User Agent** : mozilla / windows / gecko / firefox / ggpht / googleimageproxy

  - **Media Distanza** : 38.64

  - **Conteggio totale** : 11



* **User Agent** : mozilla / windows / gecko / firefox / likewise

  - **Media Distanza** : 62.88

  - **Conteggio totale** : 2



* **User Agent** : mozilla / windows / trident / lcte / like / gecko

  - **Media Distanza** : 96.91

  - **Conteggio totale** : 1



* **User Agent** : mozilla / windows / trident / like / gecko

  - **Media Distanza** : 39.84

  - **Conteggio totale** : 1



* **User Agent** : mozilla / winnt

  - **Media Distanza** : 88.66

  - **Conteggio totale** : 1
</details>


### Cluster 7
Cluster 7 represents sessions from Axios, and we can label this traffic as **Programmatic Traffic**
<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : axios

  - **Media Distanza** : 2.15

  - **Conteggio totale** : 78
  
  </details>
  
### Cluster 8
Cluster 8 represents sessions from Petal Bot, and we can label this traffic as **Programmatic Traffic**
<details> 

<summary>  Expand details : </summary>
  
  * **User Agent** : mozilla / compatible / petalbot / https / webmaster / petalsearch / site / petalbot

  - **Media Distanza** : 5.84

  - **Conteggio totale** : 13



* **User Agent** : mozilla / linux / android / applewebkit / khtml / like / gecko / mobile / safari / compatible / petalbot / https / webmaster / petalsearch / site / petalbot

  - **Media Distanza** : 1.88

  - **Conteggio totale** : 273



* **User Agent** : mozilla / linux / android / build / huaweiana / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / huawei / anyoffice / huawei / works

  - **Media Distanza** : 111.17

  - **Conteggio totale** : 2



* **User Agent** : mozilla / linux / build / applewebkit / khtml / like / gecko / version / chrome / mobile / safari / instagram / xiaomi / diting / qcom

  - **Media Distanza** : 153.29

  - **Conteggio totale** : 1
  
  </details>
  
### Cluster 9
Cluster 9 represents sessions from applications like curl, dart and insomnia, and we can label this traffic as **Programmatic Traffic**

<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : apple / webkit / networking / cfnetwork / darwin

  - **Media Distanza** : 146.71

  - **Conteggio totale** : 1



* **User Agent** : bbot

  - **Media Distanza** : 88.43

  - **Conteggio totale** : 1



* **User Agent** : compatible / msie / windows / trident

  - **Media Distanza** : 53.68

  - **Conteggio totale** : 1



* **User Agent** : curl

  - **Media Distanza** : 44.25

  - **Conteggio totale** : 4



* **User Agent** : dart / dart

  - **Media Distanza** : 19.41

  - **Conteggio totale** : 21



* **User Agent** : foregenix / threatview / security / auditor / threatview

  - **Media Distanza** : 176.75

  - **Conteggio totale** : 1



* **User Agent** : http / client

  - **Media Distanza** : 51.59

  - **Conteggio totale** : 1



* **User Agent** : https / github / bitinn

  - **Media Distanza** : 17.90

  - **Conteggio totale** : 49



* **User Agent** : insomnia

  - **Media Distanza** : 63.80

  - **Conteggio totale** : 2



* **User Agent** : macoutlook / build

  - **Media Distanza** : 33.76

  - **Conteggio totale** : 3



* **User Agent** : macoutlook / intelx / build

  - **Media Distanza** : 55.45

  - **Conteggio totale** : 4



* **User Agent** : microsoft / office / excel / desktop / appstore / apple / macbookpro

  - **Media Distanza** : 166.47

  - **Conteggio totale** : 1



* **User Agent** : microsoft / office / windows / mapi

  - **Media Distanza** : 76.73

  - **Conteggio totale** : 2



* **User Agent** : mobilesafari / cfnetwork / darwin

  - **Media Distanza** : 113.88

  - **Conteggio totale** : 1



* **User Agent** : mozilla

  - **Media Distanza** : 5.95

  - **Conteggio totale** : 1



* **User Agent** : mozilla / compatible / dataforseobot / https

  - **Media Distanza** : 62.82

  - **Conteggio totale** : 2



* **User Agent** : mozilla / compatible / duckduckgo / favicons / http / duckduckgo

  - **Media Distanza** : 118.67

  - **Conteggio totale** : 1



* **User Agent** : mozilla / compatible / https / headline / legal

  - **Media Distanza** : 125.05

  - **Conteggio totale** : 1



* **User Agent** : mozilla / compatible / msie / windows

  - **Media Distanza** : 36.52

  - **Conteggio totale** : 3



* **User Agent** : mozilla / compatible / msie / windows / trident

  - **Media Distanza** : 53.69

  - **Conteggio totale** : 1



* **User Agent** : mozilla / compatible / uptimerobot / http / uptimerobot

  - **Media Distanza** : 51.63

  - **Conteggio totale** : 3



* **User Agent** : mozilla / windows / gecko / firefox

  - **Media Distanza** : 8.68

  - **Conteggio totale** : 4



* **User Agent** : mozilla / zgrab

  - **Media Distanza** : 62.57

  - **Conteggio totale** : 2



* **User Agent** : node / soap

  - **Media Distanza** : 30.03

  - **Conteggio totale** : 17



* **User Agent** : office / windows / excel

  - **Media Distanza** : 40.07

  - **Conteggio totale** : 4



* **User Agent** : office / windows / outlook

  - **Media Distanza** : 10.30

  - **Conteggio totale** : 127



* **User Agent** : okhttp

  - **Media Distanza** : 4.39

  - **Conteggio totale** : 416



* **User Agent** : reactornetty

  - **Media Distanza** : 26.44

  - **Conteggio totale** : 1



* **User Agent** : safari / cfnetwork / darwin

  - **Media Distanza** : 72.05

  - **Conteggio totale** : 1



* **User Agent** : scanner / android

  - **Media Distanza** : 51.08

  - **Conteggio totale** : 3



* **User Agent** : unknown

  - **Media Distanza** : 27.10

  - **Conteggio totale** : 11
  
  </details>
  
### Cluster 10
Cluster 10 represents sessions from the mobile application of LeroyMerlin and we can label this traffic as **Human Traffic**

<details> 

<summary>  Expand details : </summary>
  
* **User Agent** : leroy / merlin / android / easymover / samsung / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 22.70

  - **Conteggio totale** : 15



* **User Agent** : leroy / merlin / android / vending / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 3.98

  - **Conteggio totale** : 4



* **User Agent** : leroy / merlin / android / vending / blade / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 88.20

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / cubot / note / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 88.92

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / edge / lite / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 47.00

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / global / nokia / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 73.82

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / google / pixel / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 34.12

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / huawei / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 12.03

  - **Conteggio totale** : 38



* **User Agent** : leroy / merlin / android / vending / oneplus / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 31.41

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / oppo / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 15.35

  - **Conteggio totale** : 29



* **User Agent** : leroy / merlin / android / vending / realme / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 33.01

  - **Conteggio totale** : 7



* **User Agent** : leroy / merlin / android / vending / samsung / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 4.07

  - **Conteggio totale** : 183



* **User Agent** : leroy / merlin / android / vending / sony / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 62.26

  - **Conteggio totale** : 2



* **User Agent** : leroy / merlin / android / vending / umidigi / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 88.19

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / wiko / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 88.19

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / xiaomi / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 7.17

  - **Conteggio totale** : 60



* **User Agent** : leroy / merlin / android / vending / xiaomi / note / lite / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 28.24

  - **Conteggio totale** : 2



* **User Agent** : leroy / merlin / android / vending / xiaomi / poco / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 62.69

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / android / vending / xiaomi / redmi / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 12.34

  - **Conteggio totale** : 2



* **User Agent** : leroy / merlin / android / vending / xiaomi / redmi / note / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 16.16

  - **Conteggio totale** : 16



* **User Agent** : leroy / merlin / android / vending / xiaomi / redmi / plus / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 37.95

  - **Conteggio totale** : 2



* **User Agent** : leroy / merlin / coloros / backuprestore / oppo / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 125.63

  - **Conteggio totale** : 1



* **User Agent** : leroy / merlin / google / android / packageinstaller / xiaomi / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 63.00

  - **Conteggio totale** : 2



* **User Agent** : leroy / merlin / standaloneinstall / samsung / android / custom / lmuser / appandroidlmit

  - **Media Distanza** : 62.44

  - **Conteggio totale** : 2



* **User Agent** : mozilla / compatible / blexbot / http / webmeup / crawler

  - **Media Distanza** : 68.86

  - **Conteggio totale** : 5



* **User Agent** : mozilla / compatible / censysinspect / https / about / censys

  - **Media Distanza** : 153.18

  - **Conteggio totale** : 1



* **User Agent** : sogou / spider / http / sogou / docs / help / webmasters

  - **Media Distanza** : 157.31

  - **Conteggio totale** : 1

</details>


### Cluster 11
Cluster 11 represents sessions from the Amazon health check service and we can label this traffic as **Programmatic Traffic**

<details> 

<summary>  Expand details : </summary>
* **User Agent** : amazon / route / health / check / service

  - **Media Distanza** : 1.80

  - **Conteggio totale** : 1280
</details>

 
## References
* https://www.sciencedirect.com/science/article/pii/S0950705121003373

* https://www.sciencedirect.com/science/article/pii/S1084804520300515

* https://www.frontiersin.org/articles/10.3389/fphy.2020.00125/full

* https://kth.diva-portal.org/smash/get/diva2:1705061/FULLTEXT01.pdf

* https://www.sciencedirect.com/science/article/pii/S1877050920320871

