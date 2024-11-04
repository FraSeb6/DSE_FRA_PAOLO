
import os.path
import zipfile
import pandas as pd
############################################
import geopandas as gpd
from shapely.geometry import Point
import networkx as nx
############################################
import urllib.request



if not os.path.exists("dataset"):
    print("Downloading dataset...\n")
    urllib.request.urlretrieve("https://drive.usercontent.google.com/download?id=1C_ZIzxojyVbuvkRAGyMdjOqXI0r3ndpT&export=download&authuser=0&confirm=t&uuid=9b7336fe-4c34-4a05-a3cb-9050910b6b37&at=AN_67v2XFPmyMPEvQZFCsujzNMW7%3A1728940914781", "dataset.zip")
    print("Dataset downloaded successfully!\n")

    print("Extracting dataset...\n")
    with zipfile.ZipFile("dataset.zip","r") as zip_ref:
        zip_ref.extractall("dataset")
    print("Dataset extracted successfully!\n")
    os.remove("dataset.zip")

global_temperature_csv               = pd.read_csv('.\\dataset\\GlobalTemperatures.csv').to_dict()
global_temperature_state_csv         = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByState.csv').to_dict()
global_temperature_country_csv       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv').to_dict()
global_temperature_majorcity_csv     = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv').to_dict()
global_temperature_city_csv          = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv').to_dict()





import matplotlib.pyplot as plt

# Load the data into DataFrame
df_city = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv')

# Convert dt column to datetime
df_city['dt'] = pd.to_datetime(df_city['dt'])

# Filter data for the required period
df_city = df_city[df_city['dt'].dt.year >= 1900]

# Group by city and calculate the temperature range
city_temp_range = df_city.groupby('City')['AverageTemperature'].agg(['min', 'max'])
city_temp_range['range'] = city_temp_range['max'] - city_temp_range['min']
city_temp_range = city_temp_range.reset_index()

# Merge the temperature range with the original data
df_city = df_city.merge(city_temp_range[['City', 'range']], on='City')

# Plotting the temperature ranges on a map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
geometry = [Point(xy) for xy in zip(df_city['Longitude'], df_city['Latitude'])]
geo_df = gpd.GeoDataFrame(df_city, geometry=geometry)

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
geo_df.plot(column='range', ax=ax, legend=True, markersize=5, cmap='coolwarm')
plt.title('Temperature Range in Major Cities (1900-Present)')
plt.show()

# Create a graph for the cities
G = nx.Graph()

# Add nodes with positions
for _, row in df_city.iterrows():
    G.add_node(row['City'], pos=(row['Longitude'], row['Latitude']), temp=row['AverageTemperature'])

# Add edges between the 3 closest cities
for city in df_city['City'].unique():
    city_data = df_city[df_city['City'] == city].iloc[0]
    city_point = Point(city_data['Longitude'], city_data['Latitude'])
    distances = df_city.apply(lambda row: city_point.distance(Point(row['Longitude'], row['Latitude'])), axis=1)
    closest_cities = distances.nsmallest(4).index[1:4]  # Exclude the city itself
    for idx in closest_cities:
        closest_city = df_city.iloc[idx]
        G.add_edge(city, closest_city['City'], weight=closest_city['AverageTemperature'])

# Find the warmest path from Beijing to Los Angeles
path = nx.shortest_path(G, source='Beijing', target='Los Angeles', weight='weight', method='dijkstra')
print("Suggested path from Beijing to Los Angeles:", path)

print("Done!")