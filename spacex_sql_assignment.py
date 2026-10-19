import sqlite3
import pandas as pd

# 1. Veri Setini İndirme ve SQLite Veritabanı Oluşturma
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(url)

# Geçici bellek (veya dosya) içi SQLite veritabanı bağlantısı
con = sqlite3.connect("my_data1.db")
cur = con.cursor()

# Veriyi SQLite tablosuna yazma
df.to_sql("SPACEXTBL", con, if_exists="replace", index=False, method="multi")

# Boş satırları temizleyerek SPACEXTABLE oluşturma
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE;")
cur.execute(
    "CREATE TABLE SPACEXTABLE AS SELECT * FROM SPACEXTBL WHERE Date IS NOT"
    " NULL;"
)


# Yardımcı SQL sorgu çalıştırıcı
def run_query(task_num, title, query):
  print(f"=== TASK {task_num}: {title} ===")
  result = pd.read_sql_query(query, con)
  print(result)
  print("\n" + "=" * 60 + "\n")


# TASK 1: Unique launch sites
run_query(
    1,
    "Benzersiz Fırlatma Sahaları",
    "SELECT DISTINCT Launch_Site FROM SPACEXTABLE;",
)

# TASK 2: 5 records where launch sites begin with 'CCA'
run_query(
    2,
    "'CCA' ile Başlayan İlk 5 Fırlatma Kaydı",
    "SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5;",
)

# TASK 3: Total payload mass carried by boosters launched by NASA (CRS)
run_query(
    3,
    "NASA (CRS) Tarafından Taşınan Toplam Faydalı Yük Kütlesi",
    "SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass FROM SPACEXTABLE WHERE"
    " Customer LIKE '%NASA (CRS)%';",
)

# TASK 4: Average payload mass carried by booster version F9 v1.1
run_query(
    4,
    "F9 v1.1 İtki Roketi Versiyonunun Ortalama Faydalı Yük Kütlesi",
    "SELECT AVG(PAYLOAD_MASS__KG_) AS Average_Payload_Mass FROM SPACEXTABLE"
    " WHERE Booster_Version LIKE 'F9 v1.1%';",
)

# TASK 5: Date when the first successful landing outcome in ground pad was achieved
run_query(
    5,
    "Kara Pedine (Ground Pad) Yapılan İlk Başarılı İniş Tarihi",
    "SELECT MIN(Date) AS First_Successful_Ground_Pad_Landing FROM SPACEXTABLE"
    " WHERE Landing_Outcome = 'Success (ground pad)';",
)

# TASK 6: Boosters which have success in drone ship and payload mass between 4000 and 6000
run_query(
    6,
    "Drone Ship'e Başarılı İnen ve Faydalı Yükü 4000-6000 kg Arasında Olan"
    " Roketler",
    "SELECT Booster_Version FROM SPACEXTABLE WHERE Landing_Outcome = 'Success"
    " (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;",
)

# TASK 7: Total number of successful and failure mission outcomes
run_query(
    7,
    "Başarılı ve Başarısız Görev Sonuçlarının Sayısı",
    "SELECT Mission_Outcome, COUNT(*) AS Count FROM SPACEXTABLE GROUP BY"
    " Mission_Outcome;",
)

# TASK 8: Booster versions that have carried the maximum payload mass
run_query(
    8,
    "Maksimum Faydalı Yük Taşıyan İtki Roketi Versiyonları",
    "SELECT DISTINCT Booster_Version FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ ="
    " (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE);",
)

# TASK 9: 2015 Yılındaki Drone Ship Başarısızlıkları
run_query(
    9,
    "2015 Yılında Drone Ship İniş Başarısızlıkları",
    "SELECT SUBSTR(Date, 6, 2) AS Month, Landing_Outcome, Booster_Version,"
    " Launch_Site FROM SPACEXTABLE WHERE SUBSTR(Date, 1, 4) = '2015' AND"
    " Landing_Outcome = 'Failure (drone ship)';",
)

# TASK 10: Rank the count of landing outcomes between 2010-06-04 and 2017-03-20
run_query(
    10,
    "2010-06-04 ve 2017-03-20 Tarihleri Arasında İniş Sonuçları Sıralaması",
    "SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTABLE WHERE"
    " Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER"
    " BY Outcome_Count DESC;",
)

con.close()