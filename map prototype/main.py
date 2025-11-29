import json
import folium
import streamlit as st
from branca.colormap import linear
from streamlit_folium import st_folium

m = folium.Map(location=[42.7, 25.4], zoom_start=7, tiles="CartoDB positron")

with open("resources/provinces.geojson", encoding="utf-8") as f:
    provinces = json.load(f)

with open("resources/ek_obl.json", encoding="utf-8") as f:
    nuts3 = json.load(f)

with open("resources/ptp01.01-30.06.2025.json", encoding="utf-8") as f:
    ptp = json.load(f)

def sofia_fix(name: str) -> str:
    if name.lower() == "софийска":
        return "софия"
    
    if name.lower() == "софия":
        return "софия (столица)"
    
    return name.lower()

stats = { sofia_fix(item[0]) : int(item[1]) for item in ptp[1:-1] }

colormap = linear.YlOrBr_06.scale(0, max(stats.values()) * 1.1)
colormap.caption = "Брой на ПТП по области за периода 01-06.2025г."

for feature in provinces["features"]:
    name = next(o for o in nuts3 if o["oblast"] == feature["properties"]["nuts3"])["name"]
    value = stats.get(name.lower(), 0)
    color = colormap(value) if value is not None else "#cccccc"

    folium.GeoJson(
        feature,
        style_function=lambda x, col=color: {
            "fillColor": col,
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.7,
        },
        highlight_function=lambda x: {
            "weight": 3,
            "color": "yellow"
        },
        tooltip=folium.Tooltip(
            f"<b>{name}</b><br>Value: {value}",
            sticky=True
        ),
    ).add_to(m)

m.add_child(colormap)

#m.save("bg_map.html")

st.set_page_config(layout="wide")
st_data = st_folium(m, width=1225, height=700)