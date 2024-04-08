import psycopg2
import threading
from storage import conn

class Article:
    def __init__(self, name, is_job, for_adult, content, link):
        self.name = name
        self.is_job = is_job
        self.for_adult = for_adult
        self.content = content
        self.link = link

class ArticleDB:
    connection = conn
    lock = threading.Lock()

    @classmethod
    def create_article_table(cls):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS articles (
                        name TEXT PRIMARY KEY,
                        is_job BOOLEAN NOT NULL,
                        for_adult BOOLEAN NOT NULL,
                        content TEXT,
                        link TEXT
                    );
                    """)
                    cls.connection.commit()

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error creating article table:", e)

    @classmethod
    def get_adult_jobs_names(cls) -> []:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT name FROM articles WHERE is_job = true AND for_adult = true")
                    names = [i[0].lower() for i in cursor.fetchall()]  # пайтон блядь поэтому ебемся с типами
                    return names if names is not None else []

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error getting adults article names:", e)

    @classmethod
    def get_child_jobs_names(cls) -> []:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT name FROM articles WHERE is_job = true AND for_adult = false")
                    names = [i[0] for i in cursor.fetchall()]  # пайтон блядь поэтому ебемся с типами
                    return names if names is not None else []

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error getting children article names:", e)

    @classmethod
    def get_all_jobs_names(cls) -> []:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT name FROM articles")
                    names = [i[0] for i in cursor.fetchall()]  # пайтон блядь поэтому ебемся с типами
                    return names if names is not None else []

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error getting all article names:", e)


    @classmethod
    def add_article(cls, article):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO articles (name, is_job,for_adult, content, link) VALUES (%s,%s, %s, %s, %s)",
                                   (article.name, article.is_job,article.for_adult, article.content, article.link)
                                   )
                    cls.connection.commit()

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error adding article:", e)

    @classmethod
    def get_article_by_name(cls, name):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM articles WHERE name = %s", (name,))
                    article_data = cursor.fetchone()
                    if article_data:
                        return Article(*article_data)
                    else:
                        return None

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error getting article by name:", e)


    @classmethod
    def delete_article_by_name(cls,name):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM articles WHERE name = %s", (name,))
                    cls.connection.commit()

        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error deleting article by name:", e)


ArticleDB.create_article_table()
