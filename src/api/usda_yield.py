import pandas as pd
import requests

def fetch_yield(api_key:str, crop:str, start_year:str, end_year:str) -> pd.DataFrame:
    """Fetches annual crop yield at the state level from USDA QuickStats."""

    base_url = "https://quickstats.nass.usda.gov/api/api_GET/"

    params = {
        "key": api_key,
        "commodity_desc": crop.upper(),
        "statisticcat_desc": "YIELD",
        "sector_desc": "CROPS",
        "source_desc": "SURVEY",
        "agg_level_desc": "STATE",
        "unit_desc": "BU / ACRE",
        "year__GE": start_year,
        "year__LE": end_year,
        "format": "JSON"
    }
    response = requests.get(url=base_url, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["data"])[["year", "commodity_desc", "Value","state_alpha", "state_name"]]

    return df