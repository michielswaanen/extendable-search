import psycopg2

class Database:
    def __init__(self, uri):
        self.uri = uri

    def connect(self):
        try:
            self.connection = psycopg2.connect(self.uri)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
            return False
        return True

    def disconnect(self):
        try:
            self.connection.close()
        except Exception as e:
            print(e)
            return False
        return True

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
        except Exception as e:
            print(e)
            return False
        return True

    def fetch_all(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False

    def fetch_one(self):
        try:
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            return False

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def rollback(self):
        try:
            self.connection.rollback()
        except Exception as e:
            print(e)
            return False
        return True