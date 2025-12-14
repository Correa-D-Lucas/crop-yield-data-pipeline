from sqlalchemy import create_engine

def engine_call(user:str, password:str, host:str, port:str, database:str):
    """"This function creates an engine to connect to Postgres"""

    engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )
    return engine 