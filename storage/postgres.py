import psycopg2
import os

# Connect to your postgres DB

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
