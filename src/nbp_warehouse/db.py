import psycopg
from psycopg.types.json import Jsonb


def insert_raw_tables(conn: psycopg.Connection, tables: list[dict], source_url: str) -> int:
    """Wstawia tabele NBP do raw_nbp_tables. Zwraca liczbę wstawionych wierszy."""
    for t in tables:
        conn.execute(
            """INSERT INTO raw_nbp_tables (table_type, effective_date, payload, source_url)
            VALUES (%s, %s, %s, %s)""",
            (t["table"], t["effectiveDate"], Jsonb(t), source_url),
        )
    return len(tables)