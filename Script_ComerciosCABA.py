import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from shapely.geometry import Point
from scipy.spatial import cKDTree

# Auxiliar functions
def get_bounds(gdf):
    bounds = [[gdf.geometry.bounds.miny.min(), gdf.geometry.bounds.minx.min()],
              [gdf.geometry.bounds.maxy.max(), gdf.geometry.bounds.maxx.max()]]
    return bounds

def find_nearest(point, candidates):
    tree = cKDTree(candidates[['lat', 'long']])
    distance, index = tree.query([point.y, point.x])
    return candidates.iloc[index]

# Shops data filtered
ruta_shapefile = 'C:/Users/keezl/Desktop/Comercios_CABA/Usos_del_Suelo_CABA.zip'
gdf = gpd.read_file(ruta_shapefile)
gdf = gdf.to_crs("EPSG:4326")
gdf_filtered = gdf[
    gdf.geometry.notnull() &
    gdf["tipo1"].isin(["UNICOMERCIAL", "MULTICOMERCIAL"]) &
    (gdf["estado"] == "ACTIVO") &
    gdf["calle"].notna() &
    gdf["puerta1"].notna()
]

#gdf_filtered = gdf_filtered.head(500)  # Limit to 500 for this example

# Banks data
df_bancos = pd.read_excel('C:/Users/keezl/Desktop/Comercios_CABA/bancos.xlsx')
df_ciudad = df_bancos[df_bancos['nombre'] == 'Banco Ciudad De Buenos Aires'].copy()
df_ciudad['lat'] = pd.to_numeric(df_ciudad['lat'], errors='coerce')
df_ciudad['long'] = pd.to_numeric(df_ciudad['long'], errors='coerce')
df_ciudad = df_ciudad.dropna(subset=['lat', 'long'])
gdf_ciudad = gpd.GeoDataFrame(
    df_ciudad, geometry=gpd.points_from_xy(df_ciudad.long, df_ciudad.lat), crs="EPSG:4326"
)

# Create map
center_lat = gdf_filtered.geometry.centroid.y.mean()
center_lon = gdf_filtered.geometry.centroid.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Create clusters for shops
marker_cluster = MarkerCluster(name="Comercios").add_to(m)

# Function to create popup/tooltip content for shops
def create_commerce_content(row, nearest_bank):
    return f"""
    <div style="font-family: sans-serif;">
        <b>{row['tipo2']}</b><br>
        {row['calle'] + ' ' + row['puerta1']}<br>
        {row['BARRIO']}<br>
        <b>Sucursal más cercana:</b> {nearest_bank['sucursal']}
    </div>
    """

excel_data = []

# Add shops to the map
for _, row in gdf_filtered.iterrows():
    if row.geometry is not None:
        centroid = row.geometry.centroid
        nearest_bank = find_nearest(centroid, df_ciudad)
        
        content = create_commerce_content(row, nearest_bank)
        
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=folium.Popup(content, max_width=300),
            tooltip=folium.Tooltip(content, style="max-width: 300px;"),
            icon=folium.Icon(color='red')
        ).add_to(marker_cluster)
        
        # Agregar datos para el Excel
        excel_data.append({
            'BARRIO': row['BARRIO'],
            'tipo1': row['tipo1'],
            'tipo2': row['tipo2'],
            'calle': row['calle'],
            'puerta': row['puerta1'],
            'sucursal_cercana': nearest_bank['sucursal']
        })

# Banks group
banco_group = folium.FeatureGroup(name="Sucursales Banco Ciudad")

# Add banks to the map
for _, row in gdf_ciudad.iterrows():
    tooltip_html = f"""
    <div style="font-family: sans-serif;">
        <b>{row['sucursal']}</b><br>
        {row['barrio']}
    </div>
    """
    folium.Marker(
        location=[row.lat, row.long],
        popup=row['nombre'],
        tooltip=folium.Tooltip(tooltip_html, style="max-width: 300px;"),
        icon=folium.Icon(color='blue', icon='bank', prefix='fa')
    ).add_to(banco_group)

# Add banks group to the map
banco_group.add_to(m)

# Fit maps vision
m.fit_bounds(get_bounds(gdf_filtered))

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save('C:/Users/keezl/Desktop/Comercios_CABA/FINAL.html')

print("Mapa guardado como FINAL.html")

# Create and save Excel
df_excel = pd.DataFrame(excel_data)
df_excel.to_excel('C:/Users/keezl/Desktop/Comercios_CABA/comercios_y_sucursales.xlsx', index=False)

print("Archivo Excel guardado como comercios_y_sucursales.xlsx")