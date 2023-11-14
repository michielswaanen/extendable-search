import psycopg2
import os
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

    def close(self):
        try:
            self.cursor.close()
        except Exception as e:
            print(e)
            return False
        return True

# Helper functions

def init_connection():
    database = Database(
        uri=os.getenv('DATABASE_URI')
    )
    database.connect()
    return database

def init_tables():
    database = init_connection()

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    tables = open(os.path.join(__location__, "tables.sql"), "r").read()
    database.query(tables)
    database.commit()

def get_video(video_id):
    database = init_connection()
    database.query(
        "SELECT * FROM videos WHERE id = %s",
        (video_id,)
    )
    video = database.fetch_one()
    return video

def save_video_to_db(job_id, name, fps, duration):
    database = init_connection()
    database.query(
        "INSERT INTO videos (job_id, name, fps, duration) VALUES (%s, %s, %s, %s) RETURNING id",
        (job_id, name, fps, duration)
    )
    database.commit()
    video = database.fetch_one()
    video_id = video[0]
    return video_id

def save_scene_to_db(video_id, start_frame, end_frame):
    database = init_connection()
    database.query(
        "INSERT INTO scenes (video_id, start_frame, end_frame) VALUES (%s, %s, %s) RETURNING id",
        (video_id, start_frame, end_frame)
    )
    database.commit()
    scene_id = database.fetch_one()
    return scene_id

def save_visual_modality_to_db(scene_id, vector):
    database = init_connection()
    database.query(
        "INSERT INTO modality_visual (scene_id, vector) VALUES (%s, %s)",
        (scene_id, vector)
    )
    database.commit()

def save_audio_modality_to_db(scene_id, vector):
    database = init_connection()
    database.query(
        "INSERT INTO modality_audio (scene_id, vector) VALUES (%s, %s)",
        (scene_id, vector)
    )
    database.commit()