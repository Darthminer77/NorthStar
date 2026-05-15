from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

print("API key loaded:", api_key is not None)