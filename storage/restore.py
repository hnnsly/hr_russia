import psycopg2
from storage import conn

class RestoringDatabase:
    connection = conn

    @classmethod
    def restore_users(cls):
        try:
            with cls.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users")
                row_count = cursor.fetchone()[0]
                if row_count == 0:
                    cursor.execute(
                        "INSERT INTO users (username, is_adult, city) VALUES (%s,%s,%s)",
                        ("hnnssssssly",True,"пасхалко 1488 хохохо")
                    )
                    cls.connection.commit()
                    print("Users table restored.")
        except psycopg2.Error as e:
            print("Error restoring users:", e)

    @classmethod
    def restore_articles(cls):
        try:
            with cls.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM articles")
                row_count = cursor.fetchone()[0]
                if row_count == 0:
                    cursor.execute(
                        "INSERT INTO articles (name, is_job, for_adult, content, link)  VALUES (%s,%s,%s,%s,%s)",
                        ("тест работа 18+", True, True,"тестовая работа для взрослых","google.com")
                    )
                    cls.connection.commit()
                    cursor.execute(
                        "INSERT INTO articles (name, is_job, for_adult, content, link)  VALUES (%s,%s,%s,%s,%s)",
                        ("тест работа до 18", True, False, "тестовая работа для подростков", "google.com")
                    )
                    cls.connection.commit()
                    print("Articles table restored.")
        except psycopg2.Error as e:
            print("Error restoring articles:", e)

    @classmethod
    def restore_messages(cls):
        try:
            with cls.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM messages")
                row_count = cursor.fetchone()[0]
                if row_count == 0:
                    cursor.execute(
                        "INSERT INTO messages (name, content)  VALUES (%s,%s)",
                        ("start","старт /help | /jobs")
                    )
                    cls.connection.commit()
                    cursor.execute(
                        "INSERT INTO messages (name, content)  VALUES (%s,%s)",
                        ("help", "хелп")
                    )
                    cls.connection.commit()
                    cursor.execute(
                        "INSERT INTO messages (name, content)  VALUES (%s,%s)",
                        ("вакансии до 18", "вакансии для деток")
                    )
                    cls.connection.commit()
                    cursor.execute(
                        "INSERT INTO messages (name, content)  VALUES (%s,%s)",
                        ("вакансии от 18", "вакансии для взрослых")
                    )
                    cls.connection.commit()
                    cursor.execute(
                        "INSERT INTO messages (name, content)  VALUES (%s,%s)",
                        ("нет ответа", "Что? /jobs")
                    )
                    cls.connection.commit()
                    print("Messages table restored.")
        except psycopg2.Error as e:
            print("Error restoring messages:", e)


RestoringDatabase.restore_users()
RestoringDatabase.restore_articles()
RestoringDatabase.restore_messages()
