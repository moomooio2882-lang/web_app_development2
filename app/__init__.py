import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    # 建立與設定 Flask 應用程式
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 非測試模式時載入實體設定
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 載入測試設定
        app.config.from_mapping(test_config)

    # 確保實體資料夾 (instance folder) 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from .routes.main import main_bp
    from .routes.comic import comic_bp
    from .routes.review import review_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(comic_bp)
    app.register_blueprint(review_bp)

    return app

def init_db():
    """初始化資料庫 (依照 schema.sql)"""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print("資料庫初始化成功！已建立 tables。")
