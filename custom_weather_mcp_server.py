from mcp.server.fastmcp import FastMCP
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Weather MCP Server")


WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")


@mcp.tool()
def get_current_weather(city: str):

    if not WEATHERSTACK_API_KEY:
        return {
            "error": "WEATHERSTACK_API_KEY is missing."
        }

    try:
        response = requests.get(
        "https://api.weatherstack.com/current",
        params={
            "query": city,
            "access_key": WEATHERSTACK_API_KEY,
            "units": "m"
            },
            timeout=20
        )
        data = response.json()
    except requests.RequestException as error:
        return {
            "error": f"Weatherstack request failed: {error}"
        }
    except ValueError:
        return {
            "error": "Weatherstack returned invalid JSON."
        }

    if response.status_code != 200 or "error" in data:
        return {
            "error": data.get("error", {}).get(
                "info",
                f"Weatherstack returned HTTP {response.status_code}."
            )
        }

    return {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temperature"],
        "feels_like_c": data["current"]["feelslike"],
        "humidity": data["current"]["humidity"],
        "condition": data["current"]["weather_descriptions"][0],
        "wind_speed_kph": data["current"]["wind_speed"]
    }


if __name__ == "__main__":
    mcp.run()