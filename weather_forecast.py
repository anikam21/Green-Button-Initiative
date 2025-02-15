import requests
import json
from datetime import datetime, timedelta

def get_weather_forecast():
    """
    Makes a GET request to a weather API and extracts the maximum temperature and precipitation.
    
    Parameters:
    - api_key: str. The API key for authentication.
    - url: str. The URL endpoint for the weather forecast API.
    
    Returns:
    - A dictionary with 'tempMax' and 'precip' if the request is successful.
    - An error message with the status code if the request fails.
    """
    # Getting the date for tomorrow
    tomorrow_date = datetime.now() + timedelta(days=1)

    # Formatting the date for tomorrow into "YYYY-MM-DD" format
    formatted_date = tomorrow_date.strftime("%Y-%m-%d")

    # Your API key
    api_key = 'NS1KQLefQnGEAOVO0TaNXHVQz'

    # URL of the endpoint
    url = url = f'https://forecast.weathersourceapis.com/v2/points/43.677128,-79.633453/days/{formatted_date}?fields=all&unitScale=METRIC'
    # Custom headers with API key
    headers = {'X-API-KEY': api_key}

    # Make a GET request with custom headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON string into a dictionary
        data = json.loads(response.text)
        
        # Extract the forecast data
        forecast_data = data.get('forecast', [])
        
        # Assuming there's at least one forecast entry
        if forecast_data:
            temp_max = forecast_data[0].get("tempMax")
            precip = forecast_data[0].get("precip")
            return temp_max, precip
        else:
            return {"error": "No forecast data available."}
    else:
        return {"error": f"Request failed with status code {response.status_code}."}
    
# temp_max, precip = get_weather_forecast()
# print (temp_max, precip)