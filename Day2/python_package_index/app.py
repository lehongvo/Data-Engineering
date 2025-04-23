"""
This is a demonstration of Python Package Management and Documentation.
The module shows how to structure a Python package, use dependencies,
and write proper documentation.

Author: Your Name
Version: 1.0.0
"""

import requests  # External package from PyPI
from typing import List, Dict, Optional
import json
from datetime import datetime
from dotenv import load_dotenv  # Add this import
import os  # Add this import

# Load environment variables
load_dotenv()


class WeatherAPI:
    """A simple weather API client.

    This class demonstrates how to create a well-documented Python class
    that uses external dependencies from PyPI.

    Attributes:
        api_key (str): The API key for accessing the weather service
        base_url (str): The base URL for the weather API
    """

    def __init__(self, api_key: str):
        """Initialize the WeatherAPI client.

        Args:
            api_key (str): The API key for authentication
        """
        self.api_key = api_key
        self.base_url = "https://api.weatherapi.com/v1"

    def get_current_weather(self, city: str) -> Dict:
        """Get current weather for a city.

        Args:
            city (str): The name of the city

        Returns:
            Dict: Weather information including temperature, condition, etc.

        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            response = requests.get(
                f"{self.base_url}/current.json", params={"key": self.api_key, "q": city}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching weather: {e}")
            return {}


class DataLogger:
    """A utility class for logging data.

    This class demonstrates proper documentation and type hints.
    """

    def __init__(self, filename: str):
        """Initialize the DataLogger.

        Args:
            filename (str): The name of the log file
        """
        self.filename = filename

    def log_data(self, data: Dict) -> None:
        """Log data to the file.

        Args:
            data (Dict): The data to log
        """
        with open(self.filename, "a") as f:
            timestamp = datetime.now().isoformat()
            json.dump({"timestamp": timestamp, "data": data}, f)
            f.write("\n")

    def read_logs(self) -> List[Dict]:
        """Read all logs from the file.

        Returns:
            List[Dict]: List of log entries
        """
        try:
            with open(self.filename, "r") as f:
                return [json.loads(line) for line in f]
        except FileNotFoundError:
            return []


def main():
    """Main function demonstrating the usage of the classes."""
    # Get API key from environment variables
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("Error: WEATHER_API_KEY not found in environment variables")
        return

    # Initialize our classes
    weather_api = WeatherAPI(api_key)
    logger = DataLogger("weather_logs.json")

    # Get and log weather data
    cities = ["London", "New York", "Tokyo"]
    for city in cities:
        print(f"Fetching weather data for {city}...")
        weather_data = weather_api.get_current_weather(city)
        if weather_data:
            logger.log_data(weather_data)
            print(f"Logged weather data for {city}")
        else:
            print(f"Failed to get weather data for {city}")

    # Read and display logs
    logs = logger.read_logs()
    print(f"\nTotal logs: {len(logs)}")

    # Display the latest weather data
    if logs:
        print("\nLatest weather data:")
        for log in logs[-3:]:  # Show last 3 entries
            city_data = log["data"]
            if "location" in city_data and "current" in city_data:
                location = city_data["location"]
                current = city_data["current"]
                print(f"\n{location['name']}, {location['country']}:")
                print(f"Temperature: {current['temp_c']}°C")
                print(f"Condition: {current['condition']['text']}")
                print(f"Time: {log['timestamp']}")


if __name__ == "__main__":
    main()

# Requirements for this project would be in requirements.txt:
"""
requests>=2.26.0
python-dotenv>=0.19.0
"""

# Or in Pipfile:
"""
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = ">=2.26.0"
python-dotenv = ">=0.19.0"

[dev-packages]
pytest = "*"
black = "*"
mypy = "*"

[requires]
python_version = "3.9"
"""
