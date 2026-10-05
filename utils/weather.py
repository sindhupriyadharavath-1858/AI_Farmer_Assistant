import os

import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


def get_weather(city):
    """
    Get current weather information for a city.
    """

    if not WEATHER_API_KEY:
        return {
            "success": False,
            "message": "Weather API key is missing."
        }

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            WEATHER_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.exceptions.HTTPError:

        return {
            "success": False,
            "message": (
                "City not found or Weather API key "
                "is invalid."
            )
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "message": "Weather service timed out."
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Weather error: {error}"
        }