import sqlite3
import os

DATABASE_PATH = os.path.join('instance', 'database.db')

class ReviewModel:
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_by_comic_id(cls, comic_id):
        """獲取特定漫畫的所有書評"""
        conn = cls.get_db_connection()
        reviews = conn.execute(
            'SELECT * FROM reviews WHERE comic_id = ? ORDER BY created_at DESC', 
            (comic_id,)
        ).fetchall()
        conn.close()
        return reviews

    @classmethod
    def create(cls, comic_id, nickname, content):
        """新增書評"""
        conn = cls.get_db_connection()
        query = 'INSERT INTO reviews (comic_id, nickname, content) VALUES (?, ?, ?)'
        cursor = conn.execute(query, (comic_id, nickname, content))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @classmethod
    def delete(cls, review_id):
        """刪除書評"""
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
        conn.commit()
        conn.close()
        return True
