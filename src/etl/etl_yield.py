import pandas as pd
from src.api.usda_yield import fetch_yield
from db.engine_call import engine_call
from sqlalchemy import text 

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read env vars
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")
YIELD_TABLE = os.getenv("YIELD_TABLE")
API_KEY = os.getenv("API_KEY")


def extract(api_key:str, crop:str, start_year:str, end_year:str) -> pd.DataFrame:
    """Extract Data from USDA NASS Using API Connection"""

    df = fetch_yield(api_key=api_key, crop=crop, start_year=start_year, end_year=end_year)
    return df 


def transform(df) -> pd.DataFrame:
    """Perform minimal Trasnformation in the Dataframe"""
    
    df.rename(columns={"Value":"value"}, inplace=True)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["state_name"] = df["state_name"].str.lower().str.strip().str.title()
    df["commodity_desc"] = df["commodity_desc"].str.lower().str.strip().str.title()
    return df

def load(df):
    """Load Transformed Dataframe into Postgres Database"""
    
    # creating db engine
    engine = engine_call(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME
    )

    # opening connection
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {DB_SCHEMA}.{YIELD_TABLE} RESTART IDENTITY"))

        df.to_sql(
            name=YIELD_TABLE,
            con=conn,
            schema=DB_SCHEMA,
            if_exists="append",
            index=False
        )
    engine.dispose()



def run_etl_yield():
    df = extract(api_key=API_KEY, crop="CORN", start_year="2021", end_year="2024")
    df = transform(df)
    load(df)