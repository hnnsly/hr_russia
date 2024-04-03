import psycopg2
import threading
from storage import postgres


class Article:
    def __init__(self, name, content, link):
        self.name = name
        self.content = content
        self.link = link


class ArticleDB:
    connection = postgres.conn
    lock = threading.Lock()
    @classmethod
    def create_article_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS articles (
                    name TEXT PRIMARY KEY,
                    content TEXT,
                    link TEXT
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error creating article table:", e)

    @classmethod
    def get_names(cls):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT name FROM articles"
                cursor.execute(select_query)
                names = cursor.fetchall()
                return names
        except psycopg2.Error as e:
            print("Error getting article names:", e)

    @classmethod
    def add_article(cls, article):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = "INSERT INTO articles (name, content, link) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (article.name, article.content, article.link))
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error adding article:", e)

    @classmethod
    def get_article_by_name(cls, name):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM articles WHERE name = %s"
                cursor.execute(select_query, (name,))
                article_data = cursor.fetchone()
                if article_data:
                    return Article(*article_data)
                else:
                    return None
        except psycopg2.Error as e:
            print("Error getting article by name:", e)


ArticleDB.create_article_table()
