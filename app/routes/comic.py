from flask import Blueprint, render_template, request

comic_bp = Blueprint('comic', __name__)

@comic_bp.route('/search')
def search():
    """搜尋結果頁面：依關鍵字顯示漫畫與相似推薦"""
    # TODO: 從 request.args 取得關鍵字
    # TODO: 呼叫 ComicModel.search() 與相似推薦邏輯
    # TODO: 渲染 comic/list.html
    pass

@comic_bp.route('/category/<category_name>')
def category(category_name):
    """分類頁面：依種類顯示漫畫列表"""
    # TODO: 呼叫 ComicModel.get_by_category()
    # TODO: 渲染 comic/list.html
    pass

@comic_bp.route('/comic/<int:comic_id>')
def detail(comic_id):
    """詳情頁面：顯示漫畫資訊、狀態與書評"""
    # TODO: 呼叫 ComicModel.get_by_id() 與 ReviewModel.get_by_comic_id()
    # TODO: 渲染 comic/detail.html
    pass
