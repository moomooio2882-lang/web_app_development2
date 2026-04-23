from flask import Blueprint, render_template, request, abort
from app.models.comic import ComicModel
from app.models.review import ReviewModel

comic_bp = Blueprint('comic', __name__)

@comic_bp.route('/search')
def search():
    """搜尋結果頁面：依關鍵字顯示漫畫與相似推薦"""
    keyword = request.args.get('q', '').strip()
    if not keyword:
        # 如果沒有關鍵字，重導向回首頁或顯示空結果
        return render_template('comic/list.html', comics=[], keyword=keyword)
    
    results = ComicModel.search(keyword)
    return render_template('comic/list.html', comics=results, keyword=keyword)

@comic_bp.route('/category/<category_name>')
def category(category_name):
    """分類頁面：依種類顯示漫畫列表"""
    comics = ComicModel.get_by_category(category_name)
    return render_template('comic/list.html', comics=comics, category=category_name)

@comic_bp.route('/comic/<int:comic_id>')
def detail(comic_id):
    """詳情頁面：顯示漫畫資訊、狀態與書評"""
    comic = ComicModel.get_by_id(comic_id)
    if not comic:
        abort(404)
        
    reviews = ReviewModel.get_by_comic_id(comic_id)
    similar = ComicModel.get_similar(comic_id)
    
    return render_template(
        'comic/detail.html', 
        comic=comic, 
        reviews=reviews, 
        similar=similar
    )
