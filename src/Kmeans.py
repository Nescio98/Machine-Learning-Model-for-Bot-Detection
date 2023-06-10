import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import numpy as np
from kneed import KneeLocator
import matplotlib.pyplot as plt

df = pd.read_csv("/sessions.csv")

df["user-agent"].fillna("unknown", inplace=True)

def get_unique_words(df):
    """
    Create a dictionary of unique words in the "user-agent" column.

    Parameters:
    - df (DataFrame): The input DataFrame.

    Returns:
    - words (list): A list of unique words.
    """
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df["user-agent"])
    words = vectorizer.get_feature_names_out()
    return words

words = get_unique_words(df)

df_bow = pd.DataFrame(X.toarray(), columns=words)

df = pd.concat([df, df_bow], axis=1)

df = df.drop("user-agent", axis=1)

def normalize_columns(df):
    """
    Normalize the numerical columns in the DataFrame.

    Parameters:
    - df (DataFrame): The input DataFrame.

    Returns:
    - df_scaled (DataFrame): The normalized DataFrame.
    """
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    return df_scaled

df_scaled = normalize_columns(df)

kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

### Evaluation for the appropriate number of cluster with Elbow Method
sse = []
for k in range(1, 50):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(df_scaled)
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, 50), sse)
plt.xticks(range(1, 50))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

### Evaluation for the appropriate number of cluster with Silhouette coefficients method
kl = KneeLocator(range(1, 50), sse, curve="convex", direction="decreasing")
kl.elbow

silhouette_coefficients = []
for k in range(2, 50):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(df_scaled)
    score = silhouette_score(df_scaled, kmeans.labels_)
    silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(range(2, 50), silhouette_coefficients)
plt.xticks(range(2, 50))
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
plt.show()


## Result found = 12
kmeans = KMeans(n_clusters=12, **kmeans_kwargs)
kmeans.fit(df_scaled)

df['Cluster'] = kmeans.predict(df_scaled)

## Evaluation of the distance between points and their centroid
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

result = df.loc[:, ['user-agent', 'Cluster']]
result["distance"] = 0

distances = [str(np.linalg.norm(df_scaled - centroids[label]))+x for x, label in zip(df_scaled, labels)]

for i, distance in enumerate(distances):
    result.at[i,"distance"] = distance

path = '/distance.csv'
with open(path, 'w', encoding='utf-8-sig') as f:
    df.to_csv(f)
