import folium, pandas

data = pandas.read_csv("data/Volcanoes.txt")

# Adding 2 different layers for world map.
map = folium.Map(location=[39.012057, -118.817774], zoom_start=5, tiles=None)
folium.raster_layers.TileLayer(tiles='openstreetmap', name='Open Street Map').add_to(map)
folium.raster_layers.TileLayer(tiles='CartoDB Voyager', name='CartoDB Voyager').add_to(map)

# FeatureGroup for each functionality.
fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")

#Popup is an html with a link to a search.
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=volcano+%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

lat = data["LAT"]
lon = data["LON"]
name = data["NAME"]
elev = data["ELEV"]


#Colors able to to choose.
['red', 'blue', 'green', 'purple', 'orange', 'darkred',
         'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
         'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
         'gray', 'black', 'lightgray']

def getColor(elevation):
    if(elevation > 4000):
        return "black"
    if(elevation > 3000):
        return "red"
    if(elevation > 2000):
        return "orange"
    if(elevation > 1000):
        return "green"
    return "lightgreen"
    

for lat, lon, name, elev in zip(data["LAT"],data["LON"], data["NAME"], data["ELEV"]):
    iframe = folium.IFrame(html=html % (name, name, str(elev)), width=160, height=80)
    fgv.add_child(folium.Marker(location=[lat, lon], radius=10, popup=folium.Popup(iframe), icon=folium.Icon(prefix="fa", icon="circle-info",  color=getColor(elev))))

fgp.add_child(folium.GeoJson(data=open("data/world.json", "r", encoding="utf-8-sig").read(),
                            style_function= lambda x: {'fillColor':'red' if x['properties']['POP2005'] < 10000000 
                                                       else 'orange' if x['properties']['POP2005'] < 20000000 else 'green'}))
map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl(name="Filter", position="bottomleft"))
map.save("result/MapVolcanoesWestCoast.html")
