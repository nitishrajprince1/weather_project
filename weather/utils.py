import json
from xml.etree.ElementTree import Element, SubElement, tostring

import requests

from weather_project.constant import WEATHER_API_KEY

URL = "https://weatherapi-com.p.rapidapi.com/current.json"
api_key = WEATHER_API_KEY


def get_weather_data(city):
    my_headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
    }
    params = {"q": city}

    try:
        response = requests.get(URL, headers=my_headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response format: {e}")
        return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def into_json_format(weather_data):
    if weather_data:
        weather = weather_data["current"]
        location = weather_data["location"]
        response = {
            "City": f"{location['name']}, {location['country']}",
            "Condition": weather["condition"]["text"],
            "Celsius": weather["temp_c"],
            "Fahrenheit": weather["temp_f"],
            "Wind": f"{weather['wind_mph']}mph, {weather['wind_kph']}kph",
            "Humidity": weather["humidity"],
            "Cloud": weather["cloud"],
        }
        json_response = json.dumps(response)

    else:
        json_response = {"error": "Failed to fetch weather data"}
    return json_response


def into_xml_format(weather_data):
    if weather_data:
        weather = weather_data["current"]
        root = Element("root")

        city = SubElement(root, "City")
        city.text = str(
            weather_data["location"]["name"] + " " + weather_data["location"][
                "country"]
        )

        condition = SubElement(root, "Condition")
        condition.text = str(weather["condition"]["text"])

        temp_in_celsius = SubElement(root, "Celsius")
        temp_in_celsius.text = str(weather["temp_c"])

        temp_in_fahrenheit = SubElement(root, "Fahrenheit")
        temp_in_fahrenheit.text = str(weather["temp_f"])

        wind = SubElement(root, "Wind")
        wind.text = str(f"{weather['wind_mph']}mph, {weather['wind_kph']}kph")

        humidity = SubElement(root, "Humidity")
        humidity.text = str(weather["humidity"])

        cloud = SubElement(root, "Cloud")
        cloud.text = str(weather["cloud"])

        xml_response = (
            '<?xml version="1.0" encoding="UTF-8" ?>\n' + tostring(root).decode()
        )
    else:
        xml_response = "<error>Failed to fetch weather data</error>"
    return xml_response
