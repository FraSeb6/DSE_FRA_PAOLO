
import os.path
import zipfile
import pandas as pd
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
global_temperature_country_df       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
global_temperature_country_csv       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv').to_dict()
global_temperature_majorcity_csv     = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv').to_dict()
global_temperature_city_csv          = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv').to_dict()


country = input("Enter the country name: ")

import matplotlib.pyplot as plt

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
