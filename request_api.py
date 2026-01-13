import subprocess
try:
    import requests
except ImportError:
    subprocess.run(["pip3", "install", "requests"])
    import requests

try:
    import geopy
    from geopy.geocoders import Nominatim
except ImportError:
    subprocess.run(["pip3", "install", "geopy"])
    import geopy
    from geopy.geocoders import Nominatim



def get_users_long_lad(permission_request):
    if permission_request:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        location = data["loc"]
        lat, lng = location.split(",")
        return [float(lat), float(lng)]
    else:
        raise TypeError("permission_request is not True and cannot continue the program.")


def request_weather(permission_request):
    location = get_users_long_lad(permission_request)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location[0],
        "longitude": location[1],
        "current_weather": True
    }

    response = requests.get(url, params=params)

    time_stamp = response.json()["current_weather"]["time"]
    temperature = response.json()["current_weather"]["temperature"]
    wind_speed = response.json()["current_weather"]["windspeed"]
    wind_direction = response.json()["current_weather"]["winddirection"]

    if response.json()["current_weather"]["is_day"] == 1:
        circadian = "day"
    else:
        circadian = "night"

    return [time_stamp.replace("T", " "), temperature, wind_speed, wind_direction, circadian]



if __name__ == "__main__":
    print(request_weather(True))



