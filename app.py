import streamlit as st
import requests
import pandas as pd
import folium

from streamlit_folium import st_folium

'''
# Predict your taxi rate
## Click the map for your destination
'''

dropoff_latitude = "40.769802"
dropoff_longitude = "-73.984365"

def get_pos(lat,lng):
    return lat,lng

m = folium.Map(location=[40.767937,-73.982155], tiles='OpenStreetMap', zoom_start=12)

m.add_child(folium.LatLngPopup())

map = st_folium(m, height=350, width=700)

if map['last_clicked'] is not None:
    data = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    dropoff_latitude = map['last_clicked']['lat']
    dropoff_longitude = map['last_clicked']['lng']



# data = {
#     "lat": [float(pickup_latitude), float(dropoff_latitude)],
#     "lon": [float(pickup_longitude), float(dropoff_longitude)]
# }
# df = pd.DataFrame(data)
# mean_lat = df['lat'].mean()
# mean_lon = df['lon'].mean()
# # Création de la carte avec folium
# m = folium.Map(location=[mean_lat, mean_lon], zoom_start=12)
# # Ajout des points de départ et d'arrivée
# folium.Marker([float(pickup_latitude), float(pickup_longitude)], tooltip='Start').add_to(m)
# folium.Marker([float(dropoff_latitude), float(dropoff_longitude)], tooltip='Stop').add_to(m)
# # Affichage de la carte dans Streamlit
# st_folium(m, width=725, height=500)


date_time = st.text_input('Date and time', "2013-07-06 17:18:00")
pickup_longitude = st.text_input("Pickup longitude", "-73.950655")
pickup_latitude = st.text_input("Pickup latitude", "40.783282")
dropoff_longitude = st.text_input("Dropoff longitude", dropoff_longitude)
dropoff_latitude = st.text_input("Dropoff latutide", dropoff_latitude)
passengers = st.text_input("Passengers count", 1)

if st.button('Confirm'):
    st.write("We're looking up your rate")
    st.write('Further clicks are not visible but are executed')

else:
    st.write('Click for price')

st.write(f"""
    - date_time: {date_time}
    - pickup_lon: {pickup_longitude}
    - pickup_lat: {pickup_latitude}
    - dropoff_lon: {dropoff_longitude}
    - dropoff_lat: {dropoff_latitude}
    - passengers: {passengers}
    """)

url = 'https://taxifare.lewagon.ai/predict'

params = {
    'pickup_datetime': date_time,
    'pickup_longitude': float(pickup_longitude),
    'pickup_latitude': float(pickup_latitude),
    'dropoff_longitude': float(dropoff_longitude),
    'dropoff_latitude': float(dropoff_latitude),
    'passenger_count': int(passengers)
}

response = requests.get(url, params=params)
pred = response.json() #=> {wait: 64}


st.success(f"Your rate will be: {round(pred['fare'], 2)}$")

data = {
    "lat": [float(pickup_latitude), float(dropoff_latitude)],
    "lon": [float(pickup_longitude), float(dropoff_longitude)]
}
df = pd.DataFrame(data)
mean_lat = df['lat'].mean()
mean_lon = df['lon'].mean()
# Création de la carte avec folium
m = folium.Map(location=[mean_lat, mean_lon], zoom_start=12)
# Ajout des points de départ et d'arrivée
folium.Marker([float(pickup_latitude), float(pickup_longitude)], tooltip='Start').add_to(m)
folium.Marker([float(dropoff_latitude), float(dropoff_longitude)], tooltip='Stop').add_to(m)
# Affichage de la carte dans Streamlit
dest_map = st_folium(m, width=725, height=500)
if dest_map['last_clicked'] is not None:
    st.write(dest_map)
