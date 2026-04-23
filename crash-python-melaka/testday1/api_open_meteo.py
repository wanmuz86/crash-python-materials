import requests
import json

url = "https://api.open-meteo.com/v1/forecast?latitude=1.4927&longitude=103.7414&current_weather=true"
try:
    response = requests.get(url, timeout=10)
    #If no response after 10s , Raise an Exception
    response.raise_for_status()

    print("=== Current Weather ===")
    decoded_text = response.content.decode("utf-8")

    data = json.loads(decoded_text)

    print(f"Temperature: {data["current_weather"]["temperature"]} {data["current_weather_units"]["temperature"]}")
    print(f"Wind Speed: {data["current_weather"]["windspeed"]} {data["current_weather_units"]["windspeed"]}")
    print(f"Wind Direction: {data["current_weather"]["winddirection"]}{data["current_weather_units"]["winddirection"]}")

except requests.RequestException as e:
    print("Request error.")
    print(e)
except UnicodeDecodeError as e:
    print("Decoding error")
    print(e)
except json.JSONDecodeError as e:
    print("JSON conversion error")
    print(e)