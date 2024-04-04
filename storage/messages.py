import psycopg2
import threading
import storage


class Message:
    def __init__(self, name, content):
        self.name = name
        self.content = content


class MessageDB:
    connection = storage.conn
    lock = threading.Lock()

    @classmethod
    def create_message_table(cls):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        name TEXT PRIMARY KEY UNIQUE ,
                        content TEXT
                    );
                    """)
                    cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error creating message table:", e)

    @classmethod
    def add_message(cls, message):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO messages (name, content) VALUES (%s, %s)",
                                   (message.name, message.content))
                    cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error adding message:", e)

    @classmethod
    def change_message(cls,new_message):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("UPDATE messages SET content = %s WHERE name = %s",
                                   (new_message.content, new_message.name))
                    cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error changing message:", e)

    @classmethod
    def get_message_by_name(cls, name):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM messages WHERE name = %s", (name,))
                    message_data = cursor.fetchone()
                    if message_data:
                        return Message(*message_data)
                    else:
                        return None
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error getting message by name:", e)

    @classmethod
    def delete_message_by_name(cls, name):
        try:
            with cls.lock:
                with cls.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM messages WHERE name = %s", (name,))
                    cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error deleting message by name:", e)


MessageDB.create_message_table()
