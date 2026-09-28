# Modules
import logging
from Digiscrape import digi_scraper
from Irhscrape import irh_scraper
from Technoscrape import techno_scraper
from dbase import db_exe
from query import (digi_product_insert_txt,
                   ir_product_inser_txt,
                   tech_product_insert_txt,
                   history_insert_txt)
# Logging
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Executions
def main():
    logger.info("Task Started")
    logger.info("store: Digikala")
    # Products Lists
    digi_products = digi_scraper()
    logger.info("store: Iranheadphone")
    irh_products = irh_scraper()
    logger.info("store: Technolife")
    techno_products = techno_scraper()
    # Executions
    logger.info("Updating Digikala data")
    db_exe(digi_products,digi_product_insert_txt,history_insert_txt)
    logger.info("Updating Iranheadphone data")
    db_exe(irh_products,ir_product_inser_txt,history_insert_txt)
    logger.info("Updating Technolife data")
    db_exe(techno_products,tech_product_insert_txt,history_insert_txt)
    logger.info("Task Ended")

if __name__ == "__main__":
    main()