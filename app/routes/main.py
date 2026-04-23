from flask import Blueprint, render_template
from app.models.comic import ComicModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示推薦漫畫與排行榜"""
    recommended = ComicModel.get_recommended()
    leaderboard = ComicModel.get_leaderboard()
    
    return render_template(
        'index.html', 
        recommended=recommended, 
        leaderboard=leaderboard
    )
