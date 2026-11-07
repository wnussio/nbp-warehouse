from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Jsonb
from nbp_warehouse.config import Settings

from datetime import date
from nbp_warehouse.nbp_client import build_session, fetch_tables

#url='https://api.nbp.pl/api/exchangerates/tables/A/2024-01-02/2024-01-05/'

load_dotenv()
settings = Settings.from_env()

session = build_session()


data = fetch_tables(session, date(2024, 1, 2), date(2024, 1, 5))

#data=x.json()

with psycopg.connect(settings.db_conninfo) as conn:
    for t in data:
        conn.execute(
            """INSERT INTO raw_nbp_tables (table_type, effective_date, payload, source_url)
               VALUES (%s, %s, %s, %s)""",
            (t["table"], t["effectiveDate"], Jsonb(t),'nbp:tables/A'),
        )
    print(conn.execute("SELECT count(*) FROM raw_nbp_tables").fetchone())

