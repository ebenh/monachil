import csv
import requests


# rain data from .
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.html
# used dataset:
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):.25:(42.0)%5D%5B(-123.0):.25:(-113.0)%5D
# note eben: The url above had an invalid parameter, had to set stride from 0.25 to 1
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):1:(42.0)%5D%5B(-123.0):1:(-113.0)%5D

def get_rain_data(file="chirps20GlobalPentadP05_1da0_1624_398c.csv") -> list:
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        rain_data = list()
        for row in csv_reader:
            line_count += 1
            if line_count <= 2:
                # print(f'Column names are {", ".join(row)}')
                continue
            elif line_count >= 10e10:
                break
            rain_data.append(row)
        return rain_data


def get_lat_lon(city: str) -> tuple:
    response = requests.get(
        "https://nominatim.openstreetmap.org/search.php?city="
        + city
        + "&format=jsonv2&namedetails=0&addressdetails=0&limit=1"
    )
    city_data = response.json()
    c_lat = city_data[0]["lat"]
    c_lon = city_data[0]["lon"]
    return c_lat, c_lon


def get_rainy_days(rain_data: list) -> list:
    dist_thresh = 0.05
    rain_thresh = 8.0
    dates = list()
    for row in rain_data:
        t, lat, lon, rain = row
        t = t[:10]
        lat_diff = abs(float(lat) - float(c_lat))
        lon_diff = abs(float(lon) - float(c_lon))
        if rain != "NaN":
            if float(rain) >= rain_thresh:
                if lat_diff < dist_thresh:
                    if lon_diff < dist_thresh:
                        dates.append((t, rain))
    return dates


if __name__ == '__main__':
    city = str(input("Enter city name:[San Jose]") or "San Jose")
    c_lat, c_lon = get_lat_lon(city)
    rain_data = get_rain_data()
    dates = get_rainy_days(rain_data)

    # dates=sorted(list(set(dates)))
    for item in dates:
        print(item)
    print("number of rainy 5-days: " + str(len(dates)))
