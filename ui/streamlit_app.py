import streamlit as st
import pandas as pd
from pystac import Catalog
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

@st.cache_data
def load_catalog(path="demo/Isar/catalog.json"):
    return Catalog.from_file(path)

cat = load_catalog()
items = list(cat.get_all_items())

df = pd.DataFrame([{
    "id": it.id,
    "datetime": it.datetime,
    "bbox": it.bbox
} for it in items])

st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date range", [df.datetime.min(), df.datetime.max()]
)

mask = (df.datetime.dt.date >= date_range[0]) & (df.datetime.dt.date <= date_range[1])
filtered = df[mask]

st.dataframe(filtered)

m = folium.Map(location=[0,0], zoom_start=2)
for _, row in filtered.iterrows():
    folium.Rectangle(
        bounds=[[row.bbox[1], row.bbox[0]], [row.bbox[3], row.bbox[2]]],  # [lat_min, lon_min], [lat_max, lon_max]
        popup=row.id
    ).add_to(m)

st_folium(m, width=700)
