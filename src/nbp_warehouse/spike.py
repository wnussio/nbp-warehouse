from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Jsonb
from nbp_warehouse.config import Settings

from datetime import date
from nbp_warehouse.nbp_client import build_session, fetch_tables
from nbp_warehouse.dates import date_chunks



load_dotenv()
settings = Settings.from_env()

session = build_session()




with psycopg.connect(settings.db_conninfo) as conn:
        for chunk_start, chunk_end in date_chunks(date(2024, 1, 1), date(2024, 12, 31)):
            data = fetch_tables(session, chunk_start, chunk_end)
            print(chunk_start, chunk_end, len(data))
            for t in data:
                conn.execute(
                    """INSERT INTO raw_nbp_tables (table_type, effective_date, payload, source_url)
                    VALUES (%s, %s, %s, %s)""",
                    (t["table"], t["effectiveDate"], Jsonb(t),'nbp:tables/A'),
                    )
        print(conn.execute("SELECT count(*) FROM raw_nbp_tables").fetchone())

