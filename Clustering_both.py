import pandas as pd  
import numpy as np   
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy import stats
from sklearn.cluster import KMeans
import datetime
from sklearn.model_selection import train_test_split
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

df = pd.read_csv("Live.csv", encoding='utf-8-sig', index_col=0)
print(df.head())
df.columns = df.columns.str.strip()
# Reset the index to convert the index (status_id) to a regular column
df.reset_index(inplace=True)

#1) Prepare the dataset for unsupervised learning

# Identify missing values
#Do not consider 0 as missing value since 0 is a valid value in this context
missing_values = df.isnull().sum()
total_values = df.shape[0]
missing_percentage = (missing_values / total_values) * 100
print("\n\nPercentage of missing values in each column:")
print(missing_percentage)

#Dropping missing columns
df.drop(columns=['Column1','Column2','Column3','Column4'], inplace=True)
print(df.head())


#HANDLING CATEGORICAL DATA

#2) Identify and drop the variables that have unique value to every instance of the data as it doesn't any add value to the data.

# Threshold for percentage of unique values
threshold = 98.0

# Identify categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns

for col in categorical_columns:
    # Calculate the percentage of unique values
    unique_percentage = df[col].nunique() / df.shape[0] * 100
    print(f"Percentage of unique values in {col}: {unique_percentage:.2f}%")
    # Check if the percentage exceeds the threshold
    if unique_percentage > threshold:
        # Drop the column
        df.drop(columns=[col], inplace=True)
print(df.head())

# Perform one-hot encoding for the column 'status_type'
encoder = OneHotEncoder()
status_type_encoded = encoder.fit_transform(df[['status_type']])
status_type_encoded_df = pd.DataFrame(status_type_encoded.toarray(), columns=encoder.categories_[0])
    
# Concatenate the encoded 'status_type' column with the original DataFrame
df_encoded = pd.concat([df, status_type_encoded_df], axis=1)
# Drop the original 'status_type' column
df_encoded.drop(columns=['status_type'], inplace=True)

# Display the first few rows of the encoded DataFrame
print(df_encoded.head())

# Feature Scaling
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(df_encoded)
df_scaled = pd.DataFrame(scaled_features, columns=df_encoded.columns)
print(df_scaled.head())

# HIERARCHICAL CLUSTERING

#3) Identify the optimal number of clusters that can possibly be present in the dataset

# Using dendrogram to find the optimal number of clusters
linkage_matrix = linkage(df_scaled, method='ward', metric='euclidean')
plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix, p=10, truncate_mode='level')
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Sample Index or (Cluster Size)')
plt.ylabel('Distance')
plt.show()

#Hence, from the graph we get the optimal number of clusters as 2.

# 4) Group the Facebook Live posts into different clusters and identify the status_type (Majority) of each cluster

# Initialize Agglomerative Clustering with 2 clusters
hc = AgglomerativeClustering(n_clusters=2, linkage='ward')
clusters = hc.fit_predict(df_scaled)

# Add cluster labels to the original DataFrame
df['Cluster'] = clusters
# Group by cluster and count the occurrences of each status_type
cluster_counts = df.groupby(['Cluster', 'status_type']).size().reset_index(name='Count')
# Find the majority status_type for each cluster
majority_status_type = cluster_counts.loc[cluster_counts.groupby('Cluster')['Count'].idxmax()]
print(majority_status_type)

#Visualization of clusters
plt.scatter(df_scaled.to_numpy()[clusters == 0, 0], df_scaled.to_numpy()[clusters == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(df_scaled.to_numpy()[clusters == 1, 0], df_scaled.to_numpy()[clusters == 1, 1], s=100, c='blue', label='Cluster 2')
plt.title('Clusters')
plt.legend()
plt.show()

#K MEANS CLUSTERING

#3)Identify the optimal number of clusters that can possibly be present in the dataset

# Using the elbow method to find the optimal number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)

# Plot the elbow curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
plt.xticks(range(1, 11))
plt.grid(True)
plt.show()

#Hence, from the graph we get optimal number of clusters as 2.

# 4) Group the Facebook Live posts into different clusters and identify the status_type (Majority) of each cluster

# Training the K-Means model on the dataset
kmeans = KMeans(n_clusters=2, init='k-means++', random_state=42)
y_kmeans = kmeans.fit_predict(df_scaled)

# Add cluster labels to the original DataFrame
df['Cluster'] = y_kmeans
# Group by cluster and status_type, and count the occurrences of each status_type in each cluster
cluster_counts = df.groupby(['Cluster', 'status_type']).size().reset_index(name='Count')
# Find the majority status_type for each cluster
majority_status_type = cluster_counts.loc[cluster_counts.groupby('Cluster')['Count'].idxmax()]
# Print the majority status_type for each cluster
print(majority_status_type)

#Visualization of clusters
plt.scatter(df_scaled.to_numpy()[y_kmeans == 0, 0], df_scaled.to_numpy()[y_kmeans == 0, 1], s=100, c='blue', label='Cluster 1')
plt.scatter(df_scaled.to_numpy()[y_kmeans == 1, 0], df_scaled.to_numpy()[y_kmeans == 1, 1], s=100, c='red', label='Cluster 2')
plt.title('Clusters')
plt.legend()
plt.show()


