from flask import Blueprint, request, redirect, url_for, flash
from app.models.review import ReviewModel

review_bp = Blueprint('review', __name__)

@review_bp.route('/comic/<int:comic_id>/review', methods=['POST'])
def add_review(comic_id):
    """提交書評：接收表單並存入資料庫"""
    nickname = request.form.get('nickname', '').strip()
    content = request.form.get('content', '').strip()
    
    # 簡易輸入驗證
    if not nickname or not content:
        flash("暱稱與內容皆為必填欄位！", "error")
        return redirect(url_for('comic.detail', comic_id=comic_id))
    
    success = ReviewModel.create(comic_id, nickname, content)
    
    if success:
        flash("書評發佈成功！", "success")
    else:
        flash("發佈失敗，請稍後再試。", "error")
        
    return redirect(url_for('comic.detail', comic_id=comic_id))
