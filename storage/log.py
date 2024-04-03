import threading

import psycopg2


from storage import postgres


class Log:
    def __init__(self, username, interaction, content, time):
        self.username = username
        self.interaction = interaction
        self.content = content
        self.time = time

class LogDB:
    connection = postgres.conn
    lock = threading.Lock()
    @classmethod
    def create_log_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    interaction TEXT,
                    content TEXT,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error creating log table:", e)

    @classmethod
    def add_log(cls, log):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = "INSERT INTO logs (username, interaction, content) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (log.username, log.interaction, log.content))
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error adding log:", e)

    @classmethod
    def get_unique_usernames(cls):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT DISTINCT username FROM logs"
                cursor.execute(select_query)
                usernames = cursor.fetchall()
                return usernames
        except psycopg2.Error as e:
            print("Error getting unique usernames:", e)

    @classmethod
    def get_last_interactions(cls, username):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM logs WHERE username = %s ORDER BY time DESC LIMIT 20"
                cursor.execute(select_query, (username,))
                actions = cursor.fetchall()
                return actions
        except psycopg2.Error as e:
            print("Error getting last 20 actions by username:", e)
