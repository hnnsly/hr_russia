import threading
import psycopg2
import storage


class User:
    def __init__(self, username, is_adult, city):
        self.username = username
        self.is_adult = is_adult
        self.city = city


class UserDB:
    connection = storage.conn
    lock = threading.Lock()

    @classmethod
    def create_user_table(cls) -> None:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        is_adult BOOLEAN,
                        city VARCHAR(255)
                    );
                    """)
                    cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error creating user table:", e)

    @classmethod
    def get_user_age(cls, username) -> int | bool:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("SELECT is_adult FROM users WHERE username = %s", (username,))
                    age = cursor.fetchone()
                    if age is not None:
                        return 30 if age else 20
                    return False
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error getting user by username:", e)
            return False

    @classmethod
    def check_user_existance(cls,username) -> bool:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                    cls.connection.commit()
                    username = cursor.fetchone()
                    if username is not None:
                        return True
                    else:
                        return False
        except psycopg2.Error as e:
            print("Error checking user:", e)
            cls.connection.rollback()
            return False

    @classmethod
    def add_user(cls, username, is_adult) -> bool:
        if cls.check_user_existance(username):
            try:
                with cls.lock:
                    with cls.connection.cursor() as cursor:
                        cursor.execute("""INSERT INTO users (username, is_adult) VALUES (%s,%s)""", (username, is_adult))
                        cls.connection.commit()
                        return True
            except psycopg2.Error as e:
                print("Error adding user:", e)
                cls.connection.rollback()
                return False

    @classmethod
    def change_user_age(cls, username, is_adult) -> bool:
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("""UPDATE users SET is_adult = %s WHERE username = %s""", (is_adult,username))
                    cls.connection.commit()
                    return True
        except psycopg2.Error as e:
            print("Error changing user:", e)
            cls.connection.rollback()
            return False


UserDB.create_user_table()
