import threading

import psycopg2

from storage import postgres


class User:
    def __init__(self,user_id,username,is_adult,city):
        self.user_id = user_id
        self.username = username
        self.is_adult = is_adult
        self.city = city


class UserDB:
    connection = postgres.conn
    lock = threading.Lock()

    @classmethod
    def create_user_table(cls) -> None:
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    is_adult BOOLEAN,
                    city VARCHAR(255)
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
                cursor.close()
        except psycopg2.Error as e:
            cls.connection.rollback()
            cursor.close()
            print("Error creating user table:", e)

    @classmethod
    def get_user(cls, username) -> User | bool:
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(select_query, (username,))
                user_data = cursor.fetchone()
                if user_data:
                    cursor.close()
                    return User(*user_data)
                cursor.close()
                return False
        except psycopg2.Error as e:
            cls.connection.rollback()
            cursor.close()
            print("Error getting user by username:", e)
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return False


    @classmethod
    def add_user(cls, username) -> bool | None:
        try:
            with cls.connection.cursor() as cursor:
                insert_query = ("""INSERT INTO users (username) VALUES (%s)""")
                cursor.execute(insert_query, ())
                user_id = cursor.fetchone()[0]
                cls.connection.commit()
                cursor.close()
                return True
        except psycopg2.Error as e:
            print("Error adding user:", e)
            cls.connection.rollback()
            cursor.close()
            return False
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return False
