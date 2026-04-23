import sqlite3
import os
import logging

DATABASE_PATH = os.path.join('instance', 'database.db')

class ComicModel:
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
    def get_all(cls):
        """
        獲取所有漫畫
        :return: list of sqlite3.Row
        """
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            comics = conn.execute('SELECT * FROM comics ORDER BY created_at DESC').fetchall()
            return comics
        except sqlite3.Error as e:
            logging.error(f"查詢所有漫畫失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, comic_id):
        """
        依 ID 獲取特定漫畫
        :param comic_id: 漫畫 ID (int)
        :return: sqlite3.Row or None
        """
        conn = cls.get_db_connection()
        if not conn: return None
        try:
            comic = conn.execute('SELECT * FROM comics WHERE id = ?', (comic_id,)).fetchone()
            return comic
        except sqlite3.Error as e:
            logging.error(f"查詢 ID {comic_id} 失敗: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_recommended(cls):
        """獲取首頁推薦漫畫"""
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            comics = conn.execute('SELECT * FROM comics WHERE is_recommended = 1 LIMIT 10').fetchall()
            return comics
        except sqlite3.Error as e:
            logging.error(f"獲取推薦失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_leaderboard(cls):
        """獲取排行榜 (依評分排序)"""
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            comics = conn.execute('SELECT * FROM comics ORDER BY rating DESC LIMIT 10').fetchall()
            return comics
        except sqlite3.Error as e:
            logging.error(f"獲取排行榜失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def search(cls, keyword):
        """關鍵字搜尋漫畫名稱或簡介"""
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            query = 'SELECT * FROM comics WHERE title LIKE ? OR description LIKE ?'
            comics = conn.execute(query, (f'%{keyword}%', f'%{keyword}%')).fetchall()
            return comics
        except sqlite3.Error as e:
            logging.error(f"搜尋關鍵字 '{keyword}' 失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_by_category(cls, category):
        """依種類篩選漫畫"""
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            comics = conn.execute('SELECT * FROM comics WHERE category = ?', (category,)).fetchall()
            return comics
        except sqlite3.Error as e:
            logging.error(f"篩選分類 '{category}' 失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_similar(cls, comic_id):
        """獲取相似漫畫 (同種類的其他漫畫)"""
        comic = cls.get_by_id(comic_id)
        if not comic:
            return []
        
        conn = cls.get_db_connection()
        if not conn: return []
        try:
            query = 'SELECT * FROM comics WHERE category = ? AND id != ? LIMIT 5'
            similar = conn.execute(query, (comic['category'], comic_id)).fetchall()
            return similar
        except sqlite3.Error as e:
            logging.error(f"獲取相似漫畫失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def create(cls, title, category, status, description=None, rating=0.0, cover_image=None, is_recommended=0):
        """新增漫畫"""
        conn = cls.get_db_connection()
        if not conn: return None
        try:
            query = '''
                INSERT INTO comics (title, category, status, description, rating, cover_image, is_recommended)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            cursor = conn.execute(query, (title, category, status, description, rating, cover_image, is_recommended))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"新增漫畫 '{title}' 失敗: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def update(cls, comic_id, **kwargs):
        """更新漫畫資訊"""
        if not kwargs:
            return False
        
        conn = cls.get_db_connection()
        if not conn: return False
        try:
            fields = [f"{k} = ?" for k in kwargs.keys()]
            values = list(kwargs.values())
            values.append(comic_id)
            
            query = f"UPDATE comics SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, values)
            conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"更新漫畫 ID {comic_id} 失敗: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def delete(cls, comic_id):
        """刪除漫畫"""
        conn = cls.get_db_connection()
        if not conn: return False
        try:
            conn.execute('DELETE FROM comics WHERE id = ?', (comic_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"刪除漫畫 ID {comic_id} 失敗: {e}")
            return False
        finally:
            conn.close()
