import sqlite3
import os
import logging

DATABASE_PATH = os.path.join('instance', 'database.db')

class ReviewModel:
    @staticmethod
    def get_db_connection():
        """建立並回傳資料庫連線"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logging.error(f"資料庫連線失敗: {e}")
            return None

    @classmethod
    def get_by_comic_id(cls, comic_id):
        """
        獲取特定漫畫的所有書評
        :param comic_id: 漫畫 ID
        :return: list of sqlite3.Row
        """
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            reviews = conn.execute(
                'SELECT * FROM reviews WHERE comic_id = ? ORDER BY created_at DESC', 
                (comic_id,)
            ).fetchall()
            return reviews
        except sqlite3.Error as e:
            logging.error(f"獲取漫畫 ID {comic_id} 的書評失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def create(cls, comic_id, nickname, content):
        """
        新增書評
        :param comic_id: 關聯漫畫 ID
        :param nickname: 留言者暱稱
        :param content: 書評內容
        :return: new_id or None
        """
        conn = cls.get_db_connection()
        if not conn: return None
        try:
            query = 'INSERT INTO reviews (comic_id, nickname, content) VALUES (?, ?, ?)'
            cursor = conn.execute(query, (comic_id, nickname, content))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"為漫畫 ID {comic_id} 新增書評失敗: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def delete(cls, review_id):
        """
        刪除書評
        :param review_id: 書評 ID
        :return: bool
        """
        conn = cls.get_db_connection()
        if not conn: return False
        try:
            conn.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"刪除書評 ID {review_id} 失敗: {e}")
            return False
        finally:
            conn.close()
