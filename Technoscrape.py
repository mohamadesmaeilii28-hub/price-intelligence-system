import requests as rq
import re
import logging

# Logging
logger = logging.getLogger(__name__)

# Connection Requirement
url = "https://www.technolife.com/shop_plp?page=1"
headers = { "Accept": "application/json",
            "Referer" : "https://www.technolife.com/",
            "User-Agent": "Mozilla/5.0 "}
payload ={
    "query" : """ query get_menu_products ($url: String, $filterObj: filter_obj) 
        { get_menu_products (url: $url, filterObj: $filterObj) 
            { results 
                { name _id code normal_price discount discounted_price icons { font value } 
                deadline colors image alt_image score_count score_avg available marketing_group marketing_group_id 
                warningCount show_color free_delivery start_date_discount discount_info 
                { is_permanent daily_repeat is_special_event badge_config 
                { text_color background_color icon } } discount_time is_turbo } 
                count banners { url link alt query } 
            } 
        }""",
    "variables" :  {
  "url": "category/audio-devices/headphones",
  "filterObj": {
    "page_type": "dynamic",
    "limit": 30,
    "skip": 1
  }
},
    "operationName": "get_menu_products"
}

# Functions(Main)
def techno_scraper():
    valid_list = []
    products = techno_request(url, payload, headers)
    logger.info("Validating items...")
    for p in products:
        if tech_valid(p):
            valid_list.append(p)
    logger.info("Valid items: %s", len(valid_list))
    return tech_dup_chk(valid_list)

# Request
def techno_request(_url, _payload, _headers, timeout = 10):
    # Scrape Section
    logger.info("Requesting Technolife...")
    try:
        with rq.post(_url, json=_payload, headers=_headers, timeout=timeout) as response:
            response.raise_for_status()
            techno_content = response.json()
            path = techno_content["data"]["get_menu_products"]["results"]  # 29 items due to limit
            products = []
            # Value for base
            base_prod_url = "https://www.technolife.com/product-"

            # Traverse items
            for product in path:
                # Value for code
                prod_url_code = product["code"].replace("TLP-", "")
                # Product info
                product_name = product["name"]
                if product["discounted_price"] == 0 or product["discounted_price"] is None:
                    product_price = product["normal_price"]
                else:
                    product_price = product["discounted_price"]
                availability = techno_ava(product["available"])
                # Value for slug
                _slug = product_name.lower().strip()
                _slug = re.sub(r"\s+", "-", _slug)
                _slug = re.sub(r"[^\w\-ا-ی]", "", _slug)
                product_url = gen_url(base_prod_url, prod_url_code, _slug)
                # Collect Data
                product_data = {"name": product_name,
                                "price": product_price,
                                "available": availability,
                                "url": product_url}
                products.append(product_data)
            logger.info("Collected items: %s", len(products))
            return products

    except Exception:
        logger.exception("Request Failed")
        raise

# Availability Check
def techno_ava(x):
    return x > 0

# URL generator
def gen_url(base, code, slug):
    return f"{base}{code}/{slug}"

# Validation
def tech_valid(dic):
    return (
        dic["name"] is not None and
        dic["price"] is not None and
        dic["url"] is not None)

def tech_dup_chk(li):
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
    techno_scraper()