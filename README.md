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
