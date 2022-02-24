import csv
import sys
import requests


# rain data from .
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.html
# used dataset:
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):.25:(42.0)%5D%5B(-123.0):.25:(-113.0)%5D
# note eben: The url above had an invalid parameter, had to set stride from 0.25 to 1
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):1:(42.0)%5D%5B(-123.0):1:(-113.0)%5D

def load_rain_data(filename=None) -> list:
    import pathlib
    filename = filename or pathlib.Path(__file__).parent.joinpath(
        'chirps20GlobalPentadP05_1da0_1624_398c.csv').resolve()
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=",")
        line_count = 0
        rows = list()
        for row in csv_reader:
            line_count += 1
            if line_count <= 2:
                # print(f'Column names are {", ".join(row)}')
                continue
            elif line_count >= 10e10:
                break
            rows.append(row)
        return rows


def get_lat_lon(city: str) -> tuple:
    query = {'city': city, 'format': 'jsonv2', 'namedetails': 0, 'addressdetails': 0, 'limit': 1}
    response = requests.get("https://nominatim.openstreetmap.org/search.php", query)
    response.raise_for_status()
    city_data = response.json()

    if len(city_data) == 0:
        raise ValueError(f"{city} doesn't appear to be a valid city.")

    try:
        lat = float(city_data[0]["lat"])
        lon = float(city_data[0]["lon"])
    except (KeyError, ValueError):
        raise RuntimeError('Retrieved invalid city data form web service.')

    return lat, lon


def filter_rainy_days(location: tuple, data: list, dist_thresh=0.05, rain_thresh=8.0) -> list:
    assert len(location) == 2

    rainy_days = list()
    for row in data:
        t, lat, lon, rain = row
        if rain != "NaN" and float(rain) >= rain_thresh:
            lat_diff = abs(float(lat) - location[0])
            lon_diff = abs(float(lon) - location[1])
            if lat_diff < dist_thresh and lon_diff < dist_thresh:
                rainy_days.append((t[:10], rain))
    return rainy_days


if __name__ == '__main__':
    sys.tracebacklimit = 0

    try:
        rain_data = load_rain_data()
    except FileNotFoundError:
        raise SystemExit('Rain data file not found.')

    city = str(input("Enter city name:[San Jose]") or "San Jose")

    try:
        city_lat_lon = get_lat_lon(city)
    except (ValueError, requests.exceptions.HTTPError) as e:
        raise SystemExit(e)
    except requests.exceptions.RequestException:
        raise SystemExit('Network error.')

    dates = filter_rainy_days(city_lat_lon, rain_data)

    for item in dates:
        print(item)
    print("number of rainy 5-days: " + str(len(dates)))
