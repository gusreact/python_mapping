import folium
import pandas as pd

# Create a DataFrame
data = pd.read_csv("volcano_data.csv")
lat = list(data["lat"])
lon = list(data["lon"])
name = list(data["name"])
location = list(data["location"])
status = list(data["status"])
elevation = list(data["elevation"])

def color_producer(elev):
    if elev < 1000:
        return 'green'
    elif 1000 <= elev < 3000:
        return 'orange'
    else:
        return 'red'

html = """<h4>Volcano information:</h4>
Name: %s<br>
Location: %s<br>
Status: %s<br>
Elevation: %s m
"""

map=folium.Map(location=[39.2, 0], zoom_start=2, tiles="Cartodb Positron")
fgv=folium.FeatureGroup(name="Volcanoes")
counter = 0
# Add markers to the map
for lt,ln,n,l,s,el in zip(lat, lon, name, location, status, elevation):
    iframe = folium.IFrame(html=html % (n, l, s, el), width=200, height=120)
    color = 'green'
    
    if counter % 2 == 0:    
        #If there are quotes in the string: popup=folium.Popup(str(n), parse_html=True)
        fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(el))))
    else:
        fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe), fill_color=color_producer(el), color='grey', fill_opacity=0.7))
    counter=counter + 1

fgp=folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red', 'color': 'black', 'weight': 0.5, 'fillOpacity': 0.1}))

# We need to create each FeatureGroups (one for volcanoes and one for population) to get the right functionality with the LayerControl
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
#dir(folium)
#help(folium.Marker)