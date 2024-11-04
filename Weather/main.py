
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

global_temperature_csv               = pd.read_csv('.\\dataset\\GlobalTemperatures.csv').to_dict()
global_temperature_country_df       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv')
global_temperature_country_csv       = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCountry.csv').to_dict()
global_temperature_majorcity_csv     = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByMajorCity.csv').to_dict()
global_temperature_city_csv          = pd.read_csv('.\\dataset\\GlobalLandTemperaturesByCity.csv').to_dict()


country = input("Enter the country name: ")

# Filter the data for the specified country
country_data = global_temperature_country_df[global_temperature_country_df['Country'] == country]

if country_data.empty:
    print(f"No data available for {country}")
else:
    # Convert the 'dt' column to datetime
    country_data['dt         '] = pd.to_datetime(country_data['dt         '])

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(country_data['dt         '], country_data['AverageTemperature'], label=f'Temperature in {country}')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature (°C)')
    plt.title(f'Average Temperature in {country} Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    