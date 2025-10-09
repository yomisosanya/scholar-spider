import psycopg

conn = psycopg.connect(
    dbname="publications_scraper",
    user="marc_csi_14",
    host="localhost",     
    port="5432",
    password="abc123"
)
# Import other files as modules
import base
import browse
import engine
import storage
import test
import util
import view
print("Connected successfully!")

conn.close()
