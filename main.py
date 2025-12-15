# main.py

from src.etl.etl_weather import run_etl_weather
from src.etl.etl_yield import run_etl_yield

if __name__ == "__main__":
    run_etl_weather()
    run_etl_yield()