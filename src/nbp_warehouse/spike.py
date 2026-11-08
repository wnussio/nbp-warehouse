from dotenv import load_dotenv
import psycopg
from nbp_warehouse.config import Settings

from datetime import date
from nbp_warehouse.nbp_client import build_session, fetch_tables
from nbp_warehouse.dates import date_chunks
from nbp_warehouse.db import insert_raw_tables



load_dotenv()
settings = Settings.from_env()

session = build_session()




with psycopg.connect(settings.db_conninfo) as conn:
        for chunk_start, chunk_end in date_chunks(date(2024, 1, 1), date(2024, 12, 31)):
            url,data = fetch_tables(session, chunk_start, chunk_end)
            n = insert_raw_tables(conn, data, url)
            print(chunk_start, chunk_end, n)
            
        print(conn.execute("SELECT count(*) FROM raw_nbp_tables").fetchone())

