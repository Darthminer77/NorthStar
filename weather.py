import json
import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

base_url = "https://api.openweathermap.org/data/2.5/weather"
baseforecast_url = "https://api.openweathermap.org/data/2.5/forecast"


def separator():
    print("-" * 30)


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


def current_weather(location):

    furl = f"{base_url}?q={location}&appid={api_key}&units=metric"

    try:
        fresponse = requests.get(furl, timeout=3)
        fresponse.raise_for_status()
        data = fresponse.json()

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return

    if str(data["cod"]) != "200":
        print("Error:", data["message"])
        return

    print("\nCurrent Weather")
    separator()

    city = data["name"].title()
    country = data["sys"]["country"].title()

    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]
    wind_direction = data["wind"]["deg"]

    print(f"Location     : {city}, {country}")
    print(f"Temperature  : {temperature}°C")
    print(f"Feels Like   : {feels_like}°C")
    print(f"Humidity     : {humidity}%")
    print(f"Condition    : {weather}")
    print(f"Wind Speed   : {wind_speed} m/s")
    print(f"Wind Degree  : {wind_direction}°")

    separator()
    loadhistory(location)


def forecast(location):

    furl = f"{baseforecast_url}?q={location}&appid={api_key}&units=metric"

    try:
        fresponse = requests.get(furl, timeout=3)
        fresponse.raise_for_status()
        data = fresponse.json()

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return

    if str(data["cod"]) != "200":
        print("Error:", data["message"])
        return

    print("\n5 Day Forecast")
    separator()

    city = data["city"]["name"].title()
    country = data["city"]["country"].title()

    print(f"Location: {city}, {country}\n")

    for item in data["list"][::8]:

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

        separator()


menu = {
    "1": "Current Weather",
    "2": "Forecast",
    "3": "View / Search History",
    "4": "Exit"
}

history_menu = {
    "1": "Current Weather",
    "2": "Forecast",
    "3": "Exit"
}


def menu_function():

    print("\n=== WEATHER MENU ===")

    for key, value in menu.items():
        print(f"{key}. {value}")

    option = input("Which option do you want? ")

    if option == "1":

        location = input("What is the location? ")

        current_weather(location)

    elif option == "2":

        location = input("What is the location? ")

        forecast(location)

    elif option == "3":

        history = loadhistory()

        print("\n--- HISTORY ---")

        if not history:
            print("No history found.")
            return

        for key, value in history.items():
            print(f"{key}. {value}")

        print("--- END ---")

        choice = input(
            "Select a location using the number: "
        )

        if choice not in history:
            print("Invalid option.")
            return

        location = history[choice]

        print(f"\nYou selected: {location}")

        print("\nWhat information do you want?")

        for key, value in history_menu.items():
            print(f"{key}. {value}")

        history_option = input("What option do you want? ")

        if history_option == "1":

            current_weather(location)

        elif history_option == "2":

            forecast(location)

        elif history_option == "3":

            return

        else:
            print("Invalid option.")
    elif option == "4":

        print("Goodbye.")
        sys.exit()

    else:
        print("Invalid option!")

while True:
    menu_function()