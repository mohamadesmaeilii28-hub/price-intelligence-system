# Queries

# Digikala
digi_product_insert_txt = """ INSERT INTO products
                                          (store_id, product_name, current_price, availability, product_url)
                                      VALUES (4, %s, %s, %s, %s) ON CONFLICT (store_id, product_url)
                                 DO \
                                      UPDATE SET
                                          current_price = EXCLUDED.current_price, availability = EXCLUDED.availability \
                                          RETURNING product_id"""

# Iran Headphone
ir_product_inser_txt = """ INSERT INTO products
                                           (store_id, product_name, current_price, availability, product_url)
                                       VALUES (5, %s, %s, %s, %s) ON CONFLICT (store_id, product_url)
                                             DO \
            UPDATE SET
                current_price = EXCLUDED.current_price, \
                availability = EXCLUDED.availability \
                RETURNING product_id"""

# Technolife
tech_product_insert_txt = """ INSERT INTO products
                                          (store_id, product_name, current_price, availability, product_url)
                                      VALUES (6, %s, %s, %s, %s) ON CONFLICT (store_id, product_url)
                                                 DO \
                                      UPDATE SET
                                          current_price = EXCLUDED.current_price, availability = EXCLUDED.availability \
                                          RETURNING product_id"""

# Price_history
history_insert_txt = """ INSERT INTO price_history
                                          (product_id, price)
                                      SELECT %s \
                                           , %s
                                          WHERE %s <> COALESCE (
                                           (SELECT price FROM price_history
                                          WHERE product_id = %s ORDER BY observed_at DESC LIMIT 1) \
                                           , 0)"""