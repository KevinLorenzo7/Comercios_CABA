import pandas as pd
import geopandas as gpd
import folium

# LEO EXCEL DEL GCBA CON UBICACIONES DE LOS BANCOS
df = pd.read_excel('C:/Users/keezl/Desktop/Bancos_comercios/bancos.xlsx')

""" print("Primeras 10 filas del DataFrame original:")
print(df.head(10)) """

# ME QUEDO CON LAS SUCUS DEL BANCO CIUDAD
df_filtrado = df[df['nombre'] == 'Banco Ciudad De Buenos Aires'].copy()

""" print("\nPrimeras 10 filas del DataFrame filtrado:")
print(df_filtrado.head(10))

print("\nInformación del DataFrame filtrado:")
print(df_filtrado.info()) """

# FIJO EL TIPO DE DATO NUMERICO
df_filtrado['lat'] = pd.to_numeric(df_filtrado['lat'], errors='coerce')
df_filtrado['long'] = pd.to_numeric(df_filtrado['long'], errors='coerce')

# BORRO LOS VACIOS
df_filtrado = df_filtrado.dropna(subset=['lat', 'long'])

# CREO UN GEODATAFRAME
gdf = gpd.GeoDataFrame(
    df_filtrado, geometry=gpd.points_from_xy(df_filtrado.long, df_filtrado.lat)
)

""" print("\nPrimeras 5 filas del GeoDataFrame:")
print(gdf.head())
 """
# CREO EL MAPA CENTRADO EN ARGENTINA
m = folium.Map(location=[-34.6037, -58.3816], zoom_start=10)

# AGREGO LOS MARCADORES CON SU TOOLTIP EN CADA SUCURSAL
for idx, row in gdf.iterrows():
    tooltip_html = f"""
    <div style="font-family: sans-serif;">
        <b>{row['sucursal']}</b><br>
        {row['barrio']}
    </div>
    """
    folium.Marker(
        location=[row.lat, row.long],
        popup=row['nombre'],
        tooltip=folium.Tooltip(tooltip_html, style="max-width: 300px;")
    ).add_to(m)

# GUARDA EL MAPA COMO HTML
m.save('C:/Users/keezl/Desktop/Bancos_comercios/mapa_sucursales_banco_ciudad.html')

print("El mapa ha sido creado y guardado.")