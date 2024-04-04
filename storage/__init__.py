import psycopg2
#  import os

# Connect to your postgres DB

conn = psycopg2.connect("dbname=hr_russia user=postgres password=postgres")
# conn = psycopg2.connect(os.getenv('DATABASE_URL'))
