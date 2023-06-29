from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from weather.utils import get_weather_data, into_json_format, into_xml_format


def index(request):
    return render(request, "index.html")


def get_current_weather(request):
    if request.method == "POST":
        city = request.POST.get("city", "")
        output_format = request.POST.get("output_format", "json")

        weather_data = get_weather_data(city)

        if output_format == "xml":
            data = into_xml_format(weather_data)
            return HttpResponse(data, content_type="application/xml")

        else:
            data_dict = into_json_format(weather_data)
            return HttpResponse(data_dict, content_type="application/json")

    # Return error response if weather data is not available
    return JsonResponse({"error": "Weather data not found."}, status=404)
