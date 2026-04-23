from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示推薦漫畫與排行榜"""
    # TODO: 呼叫 ComicModel 取得資料
    # TODO: 渲染 index.html
    pass
