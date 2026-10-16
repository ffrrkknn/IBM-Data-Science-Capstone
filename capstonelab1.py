# ==========================================
# 1. IMPORT LIBRARIES
# ==========================================
import requests
import pandas as pd
import numpy as np
import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# ==========================================
# 2. AUXILIARY FUNCTIONS
# ==========================================
def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])

def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])

def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])

# ==========================================
# 3. TASK 1: REQUEST AND PARSE DATA
# ==========================================
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response = requests.get(static_json_url)
print("Status Code:", response.status_code)

data = pd.json_normalize(response.json())
print(data.head())

# Filter subset
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

data['date'] = pd.to_datetime(data['date_utc']).dt.date
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# Initialize global lists
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Fetch auxiliary details safely
try:
    getBoosterVersion(data)
    getLaunchSite(data)
    getPayloadData(data)
    getCoreData(data)
except Exception as e:
    print("Canlı API erişilemedi, yedek veri seti yükleniyor...")
    backup_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
    b_df = pd.read_csv(backup_url)
    BoosterVersion = list(b_df['BoosterVersion'])
    PayloadMass = list(b_df['PayloadMass'])
    Orbit = list(b_df['Orbit'])
    LaunchSite = list(b_df['LaunchSite'])
    Outcome = list(b_df['Outcome'])
    Flights = list(b_df['Flights'])
    GridFins = list(b_df['GridFins'])
    Reused = list(b_df['Reused'])
    Legs = list(b_df['Legs'])
    LandingPad = list(b_df['LandingPad'])
    Block = list(b_df['Block'])
    ReusedCount = list(b_df['ReusedCount'])
    Serial = list(b_df['Serial'])
    Longitude = list(b_df['Longitude'])
    Latitude = list(b_df['Latitude'])

launch_dict = {
    'FlightNumber': list(data['flight_number']),
    'Date': list(data['date']),
    'BoosterVersion': BoosterVersion,
    'PayloadMass': PayloadMass,
    'Orbit': Orbit,
    'LaunchSite': LaunchSite,
    'Outcome': Outcome,
    'Flights': Flights,
    'GridFins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'LandingPad': LandingPad,
    'Block': Block,
    'ReusedCount': ReusedCount,
    'Serial': Serial,
    'Longitude': Longitude,
    'Latitude': Latitude
}

data_dict = pd.DataFrame(launch_dict)
print(data_dict.head())

# ==========================================
# 4. TASK 2: FILTER FALCON 9 LAUNCHES
# ==========================================
data_falcon9 = data_dict[data_dict['BoosterVersion'] != 'Falcon 1'].copy()
data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))
print(data_falcon9.head())

# ==========================================
# 5. TASK 3: DEALING WITH MISSING VALUES
# ==========================================
payload_mean = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'].fillna(payload_mean, inplace=True)

print("Eksik Değer Özeti:")
print(data_falcon9.isnull().sum())

# Export to CSV
data_falcon9.to_csv('dataset_part_1.csv', index=False)
print("İşlem başarıyla tamamlandı! dataset_part_1.csv kaydedildi.")