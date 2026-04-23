from flask import Blueprint, request, redirect, url_for

review_bp = Blueprint('review', __name__)

@review_bp.route('/comic/<int:comic_id>/review', methods=['POST'])
def add_review(comic_id):
    """提交書評：接收表單並存入資料庫"""
    # TODO: 從 request.form 取得暱稱與內容
    # TODO: 呼叫 ReviewModel.create()
    # TODO: 重導向回漫畫詳情頁
    pass
