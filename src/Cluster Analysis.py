import pandas as pd
from user_agents import parse

df = pd.read_csv("distance.csv", header=0) # nrows=1000

df = df.sort_values('Cluster')

def make_percentage(bots: int, humans: int):
    total = bots + humans
    bots = (bots / total) * 100
    humans = (humans / total) * 100
    if bots > humans:
        return f"{bots:.2f}% expected accuracy"
    else:
        return f"{humans:.2f}% expected accuracy"

# Make a class which stores the user agent, if the bot is a bot or not, the metadata, the mean distance and the count
class Result:
    def __init__(self, ua, is_bot, metadata, mean_distance, count):
        self.ua = ua
        #self.is_bot = is_bot
        self.is_bot = "Bot" if is_bot else "Human"
        self.metadata = metadata
        self.mean_distance = "{:.2f}".format(mean_distance)
        self.count = count

    def write_on_file(self):
        return(f"* **User Agent** : {self.ua}\n\n  - **Label** : {self.is_bot}\n\n   - **Metadata** : {self.metadata}\n\n   - **Media Distanza** : {self.mean_distance}\n\n   - **Conteggio totale** : {self.count}\n\n\n\n")



# Raggruppa i risultati per cluster e user agent e calcola la media della distanza
risultati_raggruppati = df.groupby(['Cluster', 'ua']).agg({'distance': ['mean', 'count'],"metadata":['first']})


# Apri il file risultati.txt in modalità scrittura
with open('risultati.md', 'w') as file:
    # Scrivi gli user agent per ogni cluster, la media della distanza e la conta totale
    for cluster in range(12):
        cluster_rows = risultati_raggruppati.loc[cluster]
        number_of_bots = 0
        number_of_humans = 0

        for user_agent, (media_distanza, count, metadata) in cluster_rows.iterrows():

        #for user_agent, (media_distanza, count, metadata) in cluster_rows.itertuples():
            if parse(user_agent).is_bot:
                number_of_bots += count
            else:
                number_of_humans += count
        if number_of_bots > number_of_humans: 
            file.write(f"## Cluster {cluster}:\n\n")
            file.write(f"**Programmatic traffic**:  {number_of_bots} bots, {number_of_humans} humans, {make_percentage(number_of_bots,number_of_humans)}\n\n")
        else:
            file.write(f"## Cluster {cluster}:\n\n")
            file.write(f"**Human traffic**:  {number_of_bots} bots, {number_of_humans} humans, {make_percentage(number_of_bots,number_of_humans)}\n\n")
        #print(f"Cluster {cluster}: {number_of_bots} bots, {number_of_humans} humans")

        file.write(f"<details>\n\n<summary>  Expand details : </summary>\n\n")


        cluster_rows = risultati_raggruppati.loc[cluster]
        res_list = []
        for user_agent, (media_distanza, count, metadata) in cluster_rows.iterrows():
            res_list.append(Result(user_agent, parse(user_agent).is_bot, metadata, media_distanza, count))
        # Sort the list by is_bot first
        res_list.sort(key=lambda x: x.is_bot, reverse=False)
        for res in res_list:
            file.write(res.write_on_file())
        file.write("</details>\n\n")






