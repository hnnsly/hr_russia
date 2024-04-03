from storage import postgres, users


class Logger(object):
    connection = postgres.conn
    @classmethod
    def log(cls,user:users.User) -> bool:
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