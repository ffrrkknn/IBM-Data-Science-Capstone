from math import atan2, cos, radians, sin, sqrt
import folium
from folium.features import DivIcon
from folium.plugins import MarkerCluster, MousePosition
import pandas as pd

# 1. Veri Setinin Yüklenmesi
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
spacex_df = pd.read_csv(URL)

# Harita başlangıç konumu (NASA Johnson Space Center)
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# ==========================================
# TASK 1: Mark all launch sites on a map
# ==========================================
launch_sites_df = spacex_df.groupby(["Launch Site"], as_index=False).first()
launch_sites_df = launch_sites_df[["Launch Site", "Lat", "Long"]]

for _, row in launch_sites_df.iterrows():
  coord = [row["Lat"], row["Long"]]
  site_name = row["Launch Site"]

  # Her fırlatma sahası için daire (Circle) ekleme
  circle = folium.Circle(
      location=coord, radius=1000, color="#d35400", fill=True
  ).add_child(folium.Popup(site_name))
  site_map.add_child(circle)

  # Etiket için Marker ekleme
  marker = folium.map.Marker(
      coord,
      icon=DivIcon(
          icon_size=(20, 20),
          icon_anchor=(0, 0),
          html=(
              '<div style="font-size: 12px; color:#d35400;"><b>%s</b></div>'
              % site_name
          ),
      ),
  )
  site_map.add_child(marker)

# ==========================================
# TASK 2: Mark success/failed launches on map
# ==========================================
# class=1 ise 'green', class=0 ise 'red' renklendirmesi
spacex_df["marker_color"] = spacex_df["class"].apply(
    lambda x: "green" if x == 1 else "red"
)

marker_cluster = MarkerCluster()
site_map.add_child(marker_cluster)

for index, row in spacex_df.iterrows():
  coord = [row["Lat"], row["Long"]]
  marker = folium.Marker(
      location=coord,
      icon=folium.Icon(color="white", icon_color=row["marker_color"]),
      popup=f"Site: {row['Launch Site']} | Class: {row['class']}",
  )
  marker_cluster.add_child(marker)

# ==========================================
# TASK 3: Calculate distances to proximities
# ==========================================
# Fare konumu gösterme eklentisi
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position="topright",
    separator=" Long: ",
    empty_string="NaN",
    lng_first=False,
    num_digits=20,
    prefix="Lat:",
    lat_formatter=formatter,
    lng_formatter=formatter,
)
site_map.add_child(mouse_position)


# Haversine mesafe hesaplama fonksiyonu
def calculate_distance(lat1, lon1, lat2, lon2):
  R = 6373.0  # Dünya yarıçapı (km)
  lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  return R * c


# Örnek olarak KSC LC-39A sahası ve en yakın kıyı şeridi (coastline) noktası
launch_site_lat, launch_site_lon = 28.573255, -80.646895
coastline_lat, coastline_lon = 28.56367, -80.57163

distance_coastline = calculate_distance(
    launch_site_lat, launch_site_lon, coastline_lat, coastline_lon
)

# Kıyı mesafesini gösteren etiket işareti
distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html=(
            '<div style="font-size: 12px;'
            ' color:#d35400;"><b>{:10.2f} KM</b></div>'.format(
                distance_coastline
            )
        ),
    ),
)
site_map.add_child(distance_marker)

# Fırlatma sahası ile kıyı noktası arasında çizgi (PolyLine)
lines = folium.PolyLine(
    locations=[
        [launch_site_lat, launch_site_lon],
        [coastline_lat, coastline_lon],
    ],
    weight=1,
    color="blue",
)
site_map.add_child(lines)

# Haritayı HTML olarak kaydetme
site_map.save("spacex_launch_site_map.html")
print("İşlem tamamlandı. Harita 'spacex_launch_site_map.html' olarak kaydedildi.")