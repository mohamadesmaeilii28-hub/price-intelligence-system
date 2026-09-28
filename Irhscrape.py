import requests as rq
from bs4 import BeautifulSoup
import logging

# Logging
logger = logging.getLogger(__name__
                           )
# Connection Requirements
base_url = "https://iranheadphone.com/style/over-ear-headphones"

# Functions(Main)
def irh_scraper():
    valid_list = []
    # Pagination
    for page in range(2):
        if page == 0:
            url = base_url
        else:
            url= f"{base_url}?page={page + 1}"

        ir_products = irh_request(url, 10, page+1)
        logger.info("Validating items...")
        for p in ir_products:
            if irh_valid(p):
                valid_list.append(p)
    logger.info("Valid items: %s", len(valid_list))
    return irh_dup_check(valid_list)

# Request
def irh_request(url, timeout = 10, page = None):

    logger.info("Requesting Iranheadphone page-%s...", page )
    try:
        with rq.get(url, timeout=timeout) as response:
            response.raise_for_status()
            # Object
            irh_content = response.text
            soup = BeautifulSoup(irh_content, "lxml")
            irh_products = []

            # Product Info
            products_grid = soup.find("div", class_="product-grid")
            products = products_grid.find_all("div", recursive=False)
            for p in products:
                prod_name = p.find("div", class_="name").text.strip()
                prod_url = p.find("div", class_="name").a["href"]

                price_card = p.find("div", class_="price")
                price_tag = price_card.find("span", class_="price-new")
                if price_tag:
                    prod_price = int(price_tag.get_text(strip=True).replace(
                        "تومان", "").replace(
                        ",", ""))
                else:
                    prod_price = None

                unavailable = p.find("div", class_="cart-dis")
                availability = unavailable is None
                prod_data = {"name": prod_name,
                             "price": prod_price,
                             "available": availability,
                             "url": prod_url}
                irh_products.append(prod_data)
            logger.info("Collected items from page %s: %s", page, len(irh_products))
            return irh_products

    except Exception:
        logger.exception("Request Failed")
        raise

# Validation
def irh_valid(dic):
        return (
            dic["name"] is not None and
            dic["url"] is not None and
            dic["price"] is not None
        )

# Duplication
def irh_dup_check(li):
    seen = set()
    unique = []
    dup = []
    for i in li:
        if i["url"] not in seen:
            unique.append(i)
            seen.add(i["url"])
        else:
            dup.append(i)
    return unique

if __name__ == "__main__":
    irh_scraper()