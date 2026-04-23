from app.models.comic import ComicModel
import os

# 確保 instance 資料夾存在
if not os.path.exists('instance'):
    os.makedirs('instance')

# 插入測試資料
comics = [
    {
        "title": "海賊王 ONE PIECE",
        "category": "熱血",
        "status": "連載中",
        "description": "傳奇海賊哥爾·D·羅傑在臨刑前留下了一句話，讓全世界的海賊都趨之若鶩地奔向大海。",
        "rating": 4.9,
        "is_recommended": 1,
        "cover_image": "https://images.unsplash.com/photo-1541562232579-512a21360020?w=500&q=80"
    },
    {
        "title": "咒術迴戰",
        "category": "熱血",
        "status": "已完結",
        "description": "人類產生的負面情緒，化為詛咒，潛伏於日常生活中。詛咒是蔓延於世界的禍源，最糟糕的情況下會導致人類死亡。",
        "rating": 4.7,
        "is_recommended": 1,
        "cover_image": "https://images.unsplash.com/photo-1618519764620-7403abdbbe9d?w=500&q=80"
    },
    {
        "title": "輝夜姬想讓人告白",
        "category": "戀愛",
        "status": "已完結",
        "description": "家庭背景與人品都很棒！！全日本首屈一指的名門學校・秀知院學園！！在學生會相遇的副會長・四宮輝夜與會長・白銀御行。",
        "rating": 4.8,
        "is_recommended": 0,
        "cover_image": "https://images.unsplash.com/photo-1516627145497-ae6968895b74?w=500&q=80"
    },
    {
        "title": "葬送的芙莉蓮",
        "category": "奇幻",
        "status": "連載中",
        "description": "打倒魔王「之後」的故事。魔法使芙莉蓮是長壽的精靈，她將在勇者逝去後，展開尋找人類心的旅程。",
        "rating": 4.9,
        "is_recommended": 1,
        "cover_image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500&q=80"
    }
]

for c in comics:
    ComicModel.create(**c)

print("測試資料插入成功！")
