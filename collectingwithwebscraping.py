# ==========================================
# 1. KÜTÜPHANELERİ YÜKLEME (IMPORT LIBRARIES)
# ==========================================
import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

# ==========================================
# 2. YARDIMCI FONKSİYONLAR (HELPER FUNCTIONS)
# ==========================================
def date_time(table_cells):
    """HTML tablo hücresinden tarih ve saati döndürür."""
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """HTML tablo hücresinden booster versiyonunu döndürür."""
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

def landing_status(table_cells):
    """HTML tablo hücresinden iniş durumunu döndürür."""
    out = [i for i in table_cells.strings][0]
    return out

def get_mass(table_cells):
    """HTML tablo hücresinden kütle (kg) verisini çeker."""
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

def extract_column_from_header(row):
    """Tablo başlıklarından sütun isimlerini temizleyerek ayıklar."""
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    column_name = ' '.join(row.contents)
    
    # Rakam ve boş isimleri filtrele
    if not (column_name.strip().isdigit()):
        column_name = column_name.strip()
        return column_name

# ==========================================
# 3. TASK 1: WIKIPEDIA SAYFASINI ÇEKME
# ==========================================
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# HTTP GET İsteği
response = requests.get(static_url, headers=headers)

# BeautifulSoup Nesnesi Oluşturma
soup = BeautifulSoup(response.text, 'html.parser')

# Sayfa Başlığını Yazdırma
print("Sayfa Başlığı:", soup.title.string if soup.title else "Başlık bulunamadı")

# ==========================================
# 4. TASK 2: SÜTUN İSİMLERİNİ AYIKLAMA
# ==========================================
html_tables = soup.find_all('table')
first_launch_table = html_tables[2]

column_names = []
for row in first_launch_table.find_all('th'):
    name = extract_column_from_header(row)
    if name is not None and len(name) > 0:
        column_names.append(name)

print("\nElde Edilen Sütun İsimleri:")
print(column_names)

# ==========================================
# 5. TASK 3: TABLOLARI PARSE ETME VE VERİ ÇEKME
# ==========================================
launch_dict = dict.fromkeys(column_names)

# Olası silme hatalarına karşı güvenli pop kullanımı
launch_dict.pop('Date and time ( )', None)

# Sözlük listelerini ilklendirme
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
launch_dict['Version Booster'] = []
launch_dict['Booster landing'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []

extracted_row = 0
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    for rows in table.find_all("tr"):
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
            
        row = rows.find_all('td')
        if flag:
            extracted_row += 1
            
            # Flight Number
            launch_dict['Flight No.'].append(flight_number)
            
            # Date & Time
            datatimelist = date_time(row[0])
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)
            
            time = datatimelist[1]
            launch_dict['Time'].append(time)
              
            # Booster Version
            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string if row[1].a else None
            launch_dict['Version Booster'].append(bv)
            
            # Launch Site
            launch_site = row[2].a.string if row[2].a else None
            launch_dict['Launch site'].append(launch_site)
            
            # Payload
            payload = row[3].a.string if row[3].a else None
            launch_dict['Payload'].append(payload)
            
            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            
            # Orbit
            orbit = row[5].a.string if row[5].a else None
            launch_dict['Orbit'].append(orbit)
            
            # Customer
            customer = row[6].a.string if row[6].a else None
            launch_dict['Customer'].append(customer)
            
            # Launch Outcome
            launch_outcome = list(row[7].strings)[0] if row[7].strings else None
            launch_dict['Launch outcome'].append(launch_outcome)
            
            # Booster Landing
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

# ==========================================
# 6. DATAFRAME OLUŞTURMA VE CSV EKSPORTU
# ==========================================
df = pd.DataFrame({key: pd.Series(value) for key, value in launch_dict.items()})

print("\n--- Oluşturulan Dataframe Özeti (İlk 5 Satır) ---")
print(df.head())

# CSV Olarak Kaydetme
df.to_csv('spacex_web_scraped.csv', index=False)
print("\nİşlem başarıyla tamamlandı! 'spacex_web_scraped.csv' dosyası oluşturuldu.")