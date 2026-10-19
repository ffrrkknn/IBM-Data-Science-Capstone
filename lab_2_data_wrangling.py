import numpy as np
import pandas as pd

# 1. Veri Setinin Yüklenmesi
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
)

# Eksik Değerlerin Yüzdesi
print("--- Eksik Değer Yüzdesi ---")
print(df.isnull().sum() / len(df) * 100)
print("\n--- Veri Tipleri ---")
print(df.dtypes)
print("\n" + "=" * 50 + "\n")

# TASK 1: Calculate the number of launches on each site
print("--- TASK 1: Launch Site Sayıları ---")
launch_site_counts = df["LaunchSite"].value_counts()
print(launch_site_counts)
print("\n" + "=" * 50 + "\n")

# TASK 2: Calculate the number and occurrence of each orbit
print("--- TASK 2: Orbit Sayıları ---")
orbit_counts = df["Orbit"].value_counts()
print(orbit_counts)
print("\n" + "=" * 50 + "\n")

# TASK 3: Calculate the number and occurence of mission outcome of the orbits
print("--- TASK 3: Outcome Sayıları ---")
landing_outcomes = df["Outcome"].value_counts()
print(landing_outcomes)
print("\n--- Outcome İndeksleri ---")
for i, outcome in enumerate(landing_outcomes.keys()):
  print(i, outcome)
print("\n" + "=" * 50 + "\n")

# Başarısız iniş sonuçlarının belirlenmesi
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
print("Başarısız İniş Türleri (bad_outcomes):", bad_outcomes)

# TASK 4: Create a landing outcome label from Outcome column
# Outcome bad_outcomes içinde ise 0, değilse 1
landing_class = [0 if x in bad_outcomes else 1 for x in df["Outcome"]]

# Sınıflandırma sütununun eklenmesi
df["Class"] = landing_class

print("\n--- TASK 4: Ilk 8 Satırın Class Değeri ---")
print(df[["Class"]].head(8))

print("\n--- Genel İniş Başarı Oranı (Mean Success Rate) ---")
print(df["Class"].mean())

# İşlenmiş verinin CSV olarak kaydedilmesi
df.to_csv("dataset_part_2.csv", index=False)
print("\nİşlem tamamlandı. 'dataset_part_2.csv' dosyası oluşturuldu.")