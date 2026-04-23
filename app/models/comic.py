import sqlite3
import os

DATABASE_PATH = os.path.join('instance', 'database.db')

class ComicModel:
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_all(cls):
        """獲取所有漫畫"""
        conn = cls.get_db_connection()
        comics = conn.execute('SELECT * FROM comics ORDER BY created_at DESC').fetchall()
        conn.close()
        return comics

    @classmethod
    def get_by_id(cls, comic_id):
        """依 ID 獲取特定漫畫"""
        conn = cls.get_db_connection()
        comic = conn.execute('SELECT * FROM comics WHERE id = ?', (comic_id,)).fetchone()
        conn.close()
        return comic

    @classmethod
    def get_recommended(cls):
        """獲取首頁推薦漫畫"""
        conn = cls.get_db_connection()
        comics = conn.execute('SELECT * FROM comics WHERE is_recommended = 1 LIMIT 10').fetchall()
        conn.close()
        return comics

    @classmethod
    def get_leaderboard(cls):
        """獲取排行榜 (依評分排序)"""
        conn = cls.get_db_connection()
        comics = conn.execute('SELECT * FROM comics ORDER BY rating DESC LIMIT 10').fetchall()
        conn.close()
        return comics

    @classmethod
    def search(cls, keyword):
        """關鍵字搜尋漫畫名稱或簡介"""
        conn = cls.get_db_connection()
        query = 'SELECT * FROM comics WHERE title LIKE ? OR description LIKE ?'
        comics = conn.execute(query, (f'%{keyword}%', f'%{keyword}%')).fetchall()
        conn.close()
        return comics

    @classmethod
    def get_by_category(cls, category):
        """依種類篩選漫畫"""
        conn = cls.get_db_connection()
        comics = conn.execute('SELECT * FROM comics WHERE category = ?', (category,)).fetchall()
        conn.close()
        return comics

    @classmethod
    def get_similar(cls, comic_id):
        """獲取相似漫畫 (同種類的其他漫畫)"""
        comic = cls.get_by_id(comic_id)
        if not comic:
            return []
        
        conn = cls.get_db_connection()
        query = 'SELECT * FROM comics WHERE category = ? AND id != ? LIMIT 5'
        similar = conn.execute(query, (comic['category'], comic_id)).fetchall()
        conn.close()
        return similar

    @classmethod
    def create(cls, title, category, status, description=None, rating=0.0, cover_image=None, is_recommended=0):
        """新增漫畫"""
        conn = cls.get_db_connection()
        query = '''
            INSERT INTO comics (title, category, status, description, rating, cover_image, is_recommended)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = conn.execute(query, (title, category, status, description, rating, cover_image, is_recommended))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @classmethod
    def update(cls, comic_id, **kwargs):
        """更新漫畫資訊"""
        if not kwargs:
            return False
        
        conn = cls.get_db_connection()
        fields = [f"{k} = ?" for k in kwargs.keys()]
        values = list(kwargs.values())
        values.append(comic_id)
        
        query = f"UPDATE comics SET {', '.join(fields)} WHERE id = ?"
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, comic_id):
        """刪除漫畫"""
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM comics WHERE id = ?', (comic_id,))
        conn.commit()
        conn.close()
        return True
