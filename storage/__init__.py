import psycopg2
import os

# Connect to your postgres DB

conn = psycopg2.connect("dbname=hr_russia user=postgres password=postgres")


# conn = psycopg2.connect(
#     database=os.getenv('POSTGRES_DB'),
#     user=os.getenv('POSTGRES_USER'),
#     password=os.getenv('POSTGRES_PASSWORD'),
#     host="postgres",
#     port="5432")
