import psycopg2 as pg
# import psycopg2.extras
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

# Independency
base_dir = Path(__file__).resolve().parent
# Load .env variables
load_dotenv(base_dir/".env")

# Logging
logger = logging.getLogger(__name__)

#Database Info
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
pwd = os.getenv("DB_PASS")
port_id = os.getenv("DB_PORT")

# Connection
def db_exe(prod_list, insert_txt, hist_txt):
    logger.info("Connecting to database...")
    try:
        with pg.connect( host = host,
                         dbname = database,
                         user = username,
                         password = pwd,
                         port = port_id) as conn:
            logger.info("Connection established successfully")
            with conn.cursor() as curs:
                price_detector(curs, prod_list, insert_txt, hist_txt)
            logger.info("Database update completed")
    except Exception:
        logger.exception("Database operation failed")
        raise

# Execution Function
def price_detector(cur,li, insrt, history):
    logger.info("Processing items: %s", len(li))
    for p in (li):
        p_row = (p["name"],
                 p["price"],
                 p["available"],
                 p["url"])

        cur.execute(insrt, p_row)
        product_id = cur.fetchone()[0]
        cur.execute(history, (product_id, p["price"], p["price"], product_id))