# Library
import requests as rq
import logging

# Logging
logger = logging.getLogger(__name__)

# Connection parameters
digi_url = "https://api.digikala.com/discovery/api/v2/categories/211/products?page=1&q=%D9%87%D8%AF%D9%81%D9%88%D9%86"
digi_url_headers = { "accept" : "application/json",
    "user-agent" : "Mozilla/5.0",
    "x-web-client" : "desktop",
    "x-web-client-id" : "web",
    "x-web-optimize-response" : "1"}
digi_url_params = {"page" : "1", "q" : "هدفون"}

# Functions(Main)
def digi_scraper():
    products = digi_req(digi_url, digi_url_headers, digi_url_params)
    valid_list = []
    logger.info("Validating Items...")
    for p in products:
        digi_ava(p)
        if digi_valid(p):
            valid_list.append(p)
    logger.info("Valid items: %s", len(valid_list))
    return digi_dup_valid(valid_list)

# Request
def digi_req(url, head, param):
    logger.info("Requesting Digikala...")
    try:
        with rq.get(url, headers=head, params=param, timeout=10) as response:

            response.raise_for_status()
            digi_content = response.json()  # Dict
            # Collection
            product_path = digi_content["data"]["widgets"][0]["data"]["widgets"]  # -------> Widget List
            base_url = "https://www.digikala.com"
            products = []

            # Traverse through products
            for product in product_path:
                if "default_variant" not in product["data"]:
                    continue
                product_name = product["data"]["title_fa"]
                availability = product["data"]["default_variant"]["status"]
                url = base_url + (product["data"]["url"]["uri"])
                # Price
                current_price = product["data"]["default_variant"]["price"]["selling_price"]
                product_data = {
                    "url": url,
                    "name": product_name,
                    "available": availability,
                    "price": current_price}
                # # Collect
                products.append(product_data)
            logger.info("Collected items: %s", len(products))
            return products
    except Exception:
        logger.exception("Request Failed")
        raise

# Transform
def digi_ava(dic):
    if dic["available"] == "marketable":
        dic["available"] = True
    else:
        dic["available"] = False

# Validation
def digi_valid(dic):
    return( dic["name"] is not None and
            dic["url"] is not None)

def digi_dup_valid(li):
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
    digi_scraper()