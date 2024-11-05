
import os.path
import zipfile
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt


if not os.path.exists("dataset"):
    print("Downloading dataset...\n")
    urllib.request.urlretrieve("https://drive.usercontent.google.com/download?id=1C_ZIzxojyVbuvkRAGyMdjOqXI0r3ndpT&export=download&authuser=0&confirm=t&uuid=9b7336fe-4c34-4a05-a3cb-9050910b6b37&at=AN_67v2XFPmyMPEvQZFCsujzNMW7%3A1728940914781", "dataset.zip")
    print("Dataset downloaded successfully!\n")

    print("Extracting dataset...\n")
    with zipfile.ZipFile("dataset.zip","r") as zip_ref:
        zip_ref.extractall("dataset")
    print("Dataset extracted successfully!\n")
    os.remove("dataset.zip")

global_temperature_csv                  = pd.read_csv('.\\dataset\\GlobalTemperatures.csv').to_dict()
global_temperature_country_df           = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
global_temperature_country_csv          = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv').to_dict()
global_temperature_majorcity_csv        = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv').to_dict()
# global_temperature_city_csv          = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv').to_dict()


country = input("Enter the country name: ")

country_data = pd.DataFrame()


# Filter the dataframe for the given country
country_data = global_temperature_country_df[global_temperature_country_df['Country'] == country]
#for key, value in global_temperature_country_csv.items():
# Check if the country exists in the dataset
while True:
    if country_data.empty:
        print(f"No data available for {country}. Please try again.")
        country = input("Enter the country name: ")
        country_data = global_temperature_country_df[global_temperature_country_df['Country'] == country]
    else:
        break

# Convert the 'dt' column to datetime
country_data['dt'] = pd.to_datetime(country_data['dt'])

# Ask the user for the start and end year
start_year = int(input("Enter the start year min 1750: "))
end_year = int(input("Enter the end year max 2013: "))

# Filter the data for the selected years
country_data = country_data[(country_data['dt'].dt.year >= start_year) & (country_data['dt'].dt.year <= end_year)]

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(country_data['dt'], country_data['AverageTemperature'], label='Average Temperature')
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.title(f'Average Temperature Over Time in {country} from {start_year} to {end_year}')
plt.legend()
plt.grid(True)
plt.show()





# Filter the dataframe for the given country
country_data = global_temperature_country_df[global_temperature_country_df['Country'] == country]

# Check if the country exists in the dataset
while country_data.empty:
    print(f"No data available for {country}. Please try again.")
    country = input("Enter the country name: ")
    country_data = global_temperature_country_df[global_temperature_country_df['Country'] == country]

# Convert the 'dt' column to datetime
country_data['dt'] = pd.to_datetime(country_data['dt'])

# Ask the user for the start and end year
start_year = int(input("Enter the start year min 1750: "))
end_year = int(input("Enter the end year max 2013: "))

# Filter the data for the selected years
country_data = country_data[(country_data['dt'].dt.year >= start_year) & (country_data['dt'].dt.year <= end_year)]
# Calculate the rolling mean to smooth out the data
country_data['RollingMean'] = country_data['AverageTemperature'].rolling(window=12).mean()

# Plot the data with rolling mean
plt.figure(figsize=(10, 5))
plt.plot(country_data['dt'], country_data['AverageTemperature'], label='Average Temperature', alpha=0.5)
plt.plot(country_data['dt'], country_data['RollingMean'], label='Rolling Mean (12 months)', color='red')
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.title(f'Average Temperature Over Time in {country} from {start_year} to {end_year}')
plt.legend()
plt.grid(True)
plt.show()




# Load the major city temperature data
major_city_data = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv')

# Convert the 'dt' column to datetime
major_city_data['dt'] = pd.to_datetime(major_city_data['dt'])

# Ask the user for the start and end year for city temperature range analysis
start_year_city = int(input("Enter the start year for city temperature range analysis min 1750: "))
end_year_city = int(input("Enter the end year for city temperature range analysis max 2013: "))

# Filter the data for the selected years
major_city_data = major_city_data[(major_city_data['dt'].dt.year >= start_year_city) & (major_city_data['dt'].dt.year <= end_year_city)]

# Calculate the temperature range for each city
city_temperature_range = major_city_data.groupby('City')['AverageTemperature'].agg(lambda x: x.max() - x.min()).reset_index()
city_temperature_range.columns = ['City', 'TemperatureRange']

# Sort the cities by temperature range in descending order
city_temperature_range = city_temperature_range.sort_values(by='TemperatureRange', ascending=False)

# Plot the top 10 cities with the largest temperature ranges
top_cities = city_temperature_range.head(10)

plt.figure(figsize=(12, 6))
plt.bar(top_cities['City'], top_cities['TemperatureRange'], color='orange')
plt.xlabel('City')
plt.ylabel('Temperature Range (°C)')
plt.title(f'Top 10 Cities with Largest Temperature Ranges from {start_year_city} to {end_year_city}')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()






import geopy.distance

# Load the major city temperature data
major_city_data = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv')

# Convert the 'dt' column to datetime
major_city_data['dt'] = pd.to_datetime(major_city_data['dt'])

# Filter the data for the selected years
major_city_data = major_city_data[(major_city_data['dt'].dt.year >= start_year_city) & (major_city_data['dt'].dt.year <= end_year_city)]

# Get the coordinates of the cities
city_coords = major_city_data.groupby('City').first()[['Latitude', 'Longitude']].reset_index()

# Function to find the 3 closest cities
def find_closest_cities(current_city, city_coords):
    current_coords = city_coords[city_coords['City'] == current_city][['Latitude', 'Longitude']].values[0]
    city_coords['Distance'] = city_coords.apply(lambda row: geopy.distance.distance(current_coords, (row['Latitude'], row['Longitude'])).km, axis=1)
    closest_cities = city_coords[city_coords['City'] != current_city].nsmallest(3, 'Distance')
    return closest_cities

# Function to find the warmest city among the closest cities
def find_warmest_city(closest_cities, major_city_data, current_date):
    closest_city_names = closest_cities['City'].tolist()
    temp_data = major_city_data[(major_city_data['City'].isin(closest_city_names)) & (major_city_data['dt'] == current_date)]
    warmest_city = temp_data.loc[temp_data['AverageTemperature'].idxmax()]['City']
    return warmest_city

# Initialize the route
route = ['Beijing']
current_city = 'Beijing'
current_date = major_city_data['dt'].min()

# Find the route to Los Angeles
while current_city != 'Los Angeles':
    closest_cities = find_closest_cities(current_city, city_coords)
    next_city = find_warmest_city(closest_cities, major_city_data, current_date)
    route.append(next_city)
    current_city = next_city

print("Suggested route from Beijing to Los Angeles:")
print(" -> ".join(route))