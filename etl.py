# For Sauti MySQL Database
import mysql.connector

# For labs_curs PostgreSQL Database
import urllib.parse as up
import psycopg2
from create_table import create_prices_raw
from delete_table import delete_prices_raw

# For Both
import os
from dotenv import load_dotenv
load_dotenv()

# --- Sauti DB Connection ---

sauti_conn = mysql.connector.connect(
  host=os.environ["MYSQL_HOST"],
  user=os.environ["MYSQL_USER"],
  passwd=os.environ["MYSQL_PASSWORD"],
  database=os.environ["MYSQL_DATABASE"]
)

sauti_curs = sauti_conn.cursor(buffered=True)

# --- labs_curs DB Connection ---

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

labs_conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

labs_curs =labs_conn.cursor()

# Drop Table If Exists
delete_prices_raw()
# Recreate Table
create_prices_raw()

# ---

Q = """SELECT id, 
        source,
        country,
        market,
        product_cat,
        product_agg,
        product,
        retail,
        wholesale,
        currency,
        unit,
        active
        from platform_market_prices2;
     """

sauti_curs.execute(Q)

rows = sauti_curs.fetchmany(10)

for row in rows:
  insert_row = """
  INSERT INTO prices_raw
  (id_sauti, source, country, market, product_cat,
  product_agg, product, retail, wholesale,
  currency, unit, active) VALUES """ + str(row) + """;"""
  labs_curs.execute(insert_row)



labs_conn.commit()

labs_curs.close()
labs_conn.close()

print("DS DB Connection Closed.")

sauti_curs.close()
sauti_conn.close()

print("Sauti DB Connection Closed.")