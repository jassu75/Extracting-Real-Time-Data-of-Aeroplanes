# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
from tabulate import tabulate


def get_flights_to_from_bangalore():
    lat_bang = 13.2009
    lon_bang = 77.7100
    radius = 100  # km

    url = f"https://opensky-network.org/api/states/all?lamin={lat_bang - 1}&lomin={lon_bang - 1}&lamax={lat_bang + 1}&lomax={lon_bang + 1}"

    response = requests.get(url)
    flights = []

    if response.status_code == 200:
        data = response.json()
        for state in data['states']:
            if state[5] is not None and state[6] is not None:  # Check if longitude and latitude are available
                distance_to_bangalore = haversine(lat_bang, lon_bang, state[6], state[5])
                if distance_to_bangalore <= radius:
                    # Append details for each flight
                    flights.append({
                        "ICAO": state[0],
                        "Aircraft Call": state[1].strip() if state[1] else "",
                        "Lat": state[6],
                        "Lon": state[5],
                        "Alt": state[7],
                        "GS": state[9],
                        "TAS": state[12],
                        "IAS": "N/A",  # Not provided by OpenSky
                        "Mach": state[11],
                        "ROK": state[13],
                        "TRK": state[10],
                        "HDG": state[10],  # Assuming heading is similar to track
                        "Live": state[8]
                    })
        print(tabulate(flights, headers="keys", tablefmt="github"))
    else:
        print("Failed to retrieve data")


def haversine(lat1, lon1, lat2, lon2):
    import math
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


if __name__ == "__main__":
    get_flights_to_from_bangalore()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
