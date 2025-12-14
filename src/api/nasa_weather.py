import requests
import pandas as pd


def fetch_weather_data(lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"

    params = {
        "start":start,
        "end":end,
        "latitude":lat,
        "longitude":lon,
        "community":"AG",
        "parameters":"T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "format":"JSON",
        "header":"true"
        }
    response = requests.get(url=url, params=params)
    response.raise_for_status()

    print(f"Requesting NASA POWER API:\n{response.url}\n")

    parameters = response.json()["properties"]["parameter"]

    df = pd.DataFrame({
        "date": list(parameters["T2M"].keys()),
        "temp_avg_c": list(parameters["T2M"].values()),
        "precipitation_mm": list(parameters["PRECTOTCORR"].values()),
        "solar_radiation": list(parameters["ALLSKY_SFC_SW_DWN"].values())
    })

    return df