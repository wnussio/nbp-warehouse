import argparse
import logging
from datetime import date

import psycopg
from dotenv import load_dotenv

from nbp_warehouse.config import Settings
from nbp_warehouse.dates import date_chunks
from nbp_warehouse.db import insert_raw_tables
from nbp_warehouse.nbp_client import build_session, fetch_tables


logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest NBP table A rates into raw_nbp_tables")
    parser.add_argument("--start", type=date.fromisoformat, required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", type=date.fromisoformat, required=True, help="YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger.info("Ingesting %s..%s", args.start, args.end)
    load_dotenv()
    settings = Settings.from_env()
    session = build_session()

    with psycopg.connect(settings.db_conninfo) as conn:
        total=0
        for chunk_start, chunk_end in date_chunks(args.start, args.end):
            url,data = fetch_tables(session, chunk_start, chunk_end)
            n = insert_raw_tables(conn, data, url)
            logger.info("Chunk %s..%s: inserted %d rows", chunk_start, chunk_end, n)
            total+=n
        
        logger.info("Done: inserted %d rows", total)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    main()
