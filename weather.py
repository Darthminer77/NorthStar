###
import json
import os
import requests
from dotenv import load_dotenv
###
load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

base_url = 'https://api.openweathermap.org/data/2.5/weather'
baseforecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
location = str(input("Input the location: ",  ))

def loadhistory(location=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "save.json")
    try:
        with open(file_path, "r") as file:
            locations = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        locations = {}

    if location is not None:
        location = location.upper()
        if location not in locations.values():
            next_key = str(len(locations) + 1)
            locations[next_key] = location
            with open(file_path, "w") as file:
                json.dump(locations, file, indent=4)

    return locations


def forecast():

    furl = f"{baseforecast_url}?q={location}&appid={api_key}&units=metric"
    fresponse = requests.get(furl, timeout=3)

    data = fresponse.json()
    if data["cod"] != "200":
        print("Error:", data["message"])
        return

    print("\n5 Day Forecast")
    print("-" * 30)

    city = data["city"]["name"]
    country = data["city"]["country"]

    print(f"Location: {city}, {country}\n")

    # Loop through forecast list
    for item in data["list"][::5]:
        date = item["dt_txt"]
        temperature = item["main"]["temp"]
        feels_like = item["main"]["feels_like"]
        humidity = item["main"]["humidity"]
        weather = item["weather"][0]["description"]
        wind_speed = item["wind"]["speed"]
        wind_direction = item["wind"]["deg"]
        print(f"Date         : {date}")
        print(f"Temperature  : {temperature}°C")
        print(f"Feels Like   : {feels_like}°C")
        print(f"Humidity     : {humidity}%")
        print(f"Condition    : {weather}")
        print(f"Wind Speed   : {wind_speed} m/s")
        print(f"Wind Degree  : {wind_direction}°")
        print("-" * 30)

    pass

loadhistory(location)
forecast()

history = loadhistory()
print(history)