from app import create_app, init_db
import sys

app = create_app()

if __name__ == '__main__':
    # 如果執行時帶有 init 參數，則初始化資料庫
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_db()
    else:
        app.run(debug=True)
