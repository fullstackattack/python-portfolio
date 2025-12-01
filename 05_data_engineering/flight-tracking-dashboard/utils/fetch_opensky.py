import requests
import pandas as pd

def fetch_opensky_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)

    data = response.json()
    states = data.get("states", [])

    df = pd.DataFrame(states, columns=[
        "icao24", "callsign", "origin_country", "time_position",
        "last_contact", "longitude", "latitude", "baro_altitude",
        "on_ground", "velocity", "heading", "vertical_rate",
        "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ])

    df = df.dropna(subset=["longitude", "latitude"])
    return df

