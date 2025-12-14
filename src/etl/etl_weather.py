import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import text

from src.api.nasa_weather import fetch_weather_data
from db.engine_call import engine_call

# Load environment variables
load_dotenv()

# Read env vars
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")
WEATHER_TABLE = os.getenv("WEATHER_TABLE")


# Initialize ETL
def extract(lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    """Extract weather data from NASA POWER API"""
    df = fetch_weather_data(lat, lon, start, end)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply minimal transformations"""
    df["year"] = df["date"].str[0:4].astype(int)
    df["month"] = df["date"].str[4:6].astype(int)
    df = df.drop(columns=["date"])
    df = df.query("month >= 1 and month <= 12")
    return df


def load(df: pd.DataFrame):
    """Load DataFrame into Postgres"""
    engine = engine_call(
        user=DB_USER, 
        password=DB_PASSWORD, 
        host=DB_HOST, 
        port=DB_PORT, 
        database=DB_NAME)

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {DB_SCHEMA}.{WEATHER_TABLE} RESTART IDENTITY"))

        df.to_sql(
            name=WEATHER_TABLE,
            con=conn,
            schema=DB_SCHEMA,
            if_exists="append",
            index=False
        )
    engine.dispose()


def run_etl_weather():
    df = extract(lat=38.456085, lon=-92.288368, start="2021", end="2024")
    df = transform(df)
    load(df)