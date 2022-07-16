import sqlite3

con = sqlite3.connect('data/data.db')
cur = con.cursor()
cur.execute("""CREATE TRIGGER price_change
AFTER update on offers.price
BEGIN INSERT INTO prices(
price,
time,
product_id
)
VALUES(
    offers.price,
    'UPDATE',
    DATETIME('NOW'),
    product.id
)
""")

con.commit()
