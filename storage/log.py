import threading
import psycopg2
from storage import conn

class Log:
    def __init__(self, username, interaction, content, time):
        self.username = username
        self.interaction = interaction
        self.content = content
        self.time = time

class LogDB:
    connection = conn
    lock = threading.Lock()

    @classmethod
    def create_log_table(cls):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id SERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        interaction TEXT,
                        content TEXT,
                        time TIMESTAMP
                    );
                    """)
                    cls.connection.commit()

        except psycopg2.Error as e:
            print("Error creating log table:", e)

    @classmethod
    def add_log(cls, log):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO logs (username, interaction, content) VALUES (%s, %s, %s)",
                                   (log.username, log.interaction, log.content)
                                   )
                    cls.connection.commit()

        except psycopg2.Error as e:
            print("Error adding log:", e)

    @classmethod
    def get_unique_usernames(cls):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT username FROM logs")
                    usernames = cursor.fetchall()
                    return usernames

        except psycopg2.Error as e:
            print("Error getting unique usernames:", e)

    @classmethod
    def get_last_interactions(cls, username):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM logs WHERE username = %s ORDER BY time DESC LIMIT 20",
                                   (username,)
                                   )
                    actions = cursor.fetchall()
                    return actions

        except psycopg2.Error as e:
            print("Error getting last 20 actions by username:", e)

LogDB.create_log_table()
