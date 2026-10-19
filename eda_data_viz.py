import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Veri Setinin Yüklenmesi
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
df = pd.read_csv(URL)

print("--- Veri Setinin İlk 5 Satırı ---")
print(df.head())
print("\n" + "="*60 + "\n")

# TASK 1: Visualize the relationship between Flight Number and Launch Site
plt.figure(figsize=(15, 6))
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=3)
plt.xlabel("Flight Number", fontsize=15)
plt.ylabel("Launch Site", fontsize=15)
plt.title("Flight Number vs Launch Site", fontsize=16)
plt.show()

# TASK 2: Visualize the relationship between Payload Mass and Launch Site
plt.figure(figsize=(15, 6))
sns.scatterplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=15)
plt.ylabel("Launch Site", fontsize=15)
plt.title("Payload Mass vs Launch Site", fontsize=16)
plt.show()

# TASK 3: Visualize the relationship between success rate of each orbit type
orbit_success = df.groupby("Orbit")["Class"].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(x="Orbit", y="Class", data=orbit_success)
plt.xlabel("Orbit Type", fontsize=12)
plt.ylabel("Success Rate", fontsize=12)
plt.title("Success Rate by Orbit Type", fontsize=14)
plt.show()

# TASK 4: Visualize the relationship between Flight Number and Orbit type
plt.figure(figsize=(12, 6))
sns.scatterplot(x="FlightNumber", y="Orbit", hue="Class", data=df)
plt.xlabel("Flight Number", fontsize=12)
plt.ylabel("Orbit Type", fontsize=12)
plt.title("Flight Number vs Orbit Type", fontsize=14)
plt.show()

# TASK 5: Visualize the relationship between Payload Mass and Orbit type
plt.figure(figsize=(12, 6))
sns.scatterplot(x="PayloadMass", y="Orbit", hue="Class", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=12)
plt.ylabel("Orbit Type", fontsize=12)
plt.title("Payload Mass vs Orbit Type", fontsize=14)
plt.show()

# TASK 6: Visualize the launch success yearly trend
year = []
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year

df['Year'] = Extract_year()
yearly_success = df.groupby('Year')['Class'].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.lineplot(x="Year", y="Class", data=yearly_success, marker='o')
plt.xlabel("Year", fontsize=12)
plt.ylabel("Success Rate", fontsize=12)
plt.title("Launch Success Yearly Trend", fontsize=14)
plt.grid(True)
plt.show()

# TASK 7: Create dummy variables to categorical columns
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 
               'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]

features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
print("--- One-Hot Encoded Özellikler ---")
print(features_one_hot.head())

# TASK 8: Cast all numeric columns to float64
features_one_hot = features_one_hot.astype('float64')

# CSV Olarak Dışa Aktarma
features_one_hot.to_csv('dataset_part_3.csv', index=False)
print("\nİşlem tamamlandı. Tüm sütunlar float64 tipine dönüştürüldü ve 'dataset_part_3.csv' olarak kaydedildi.")