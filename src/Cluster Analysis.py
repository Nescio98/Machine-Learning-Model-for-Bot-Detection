import pandas as pd

df = pd.read_csv("distance.csv", header=0) 
df = df.sort_values('Cluster')

grouped_results = df.groupby(['Cluster', 'user-agent']).agg({'distance': ['mean', 'count']})

# Open the file risultati.txt in write mode
with open('results.txt', 'w') as file:
    # Write user agents for each cluster, the mean distance, and the total count
    for cluster in range(12):
        file.write(f"## Cluster {cluster}:\n")
        cluster_rows = grouped_results.loc[cluster]
        for user_agent, (avg_distance, count) in cluster_rows.iterrows():
            res = "{:.2f}".format(avg_distance)
            file.write(f"**User Agent** : {user_agent}\n\n")
            file.write(f"**Avg Distance** : {res}\n\n")
            file.write(f"**Total Count** : {int(count)}\n\n")
            file.write("\n\n")
