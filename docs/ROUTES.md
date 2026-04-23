# 漫畫推薦系統 - 路由設計文件 (Routes)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 推薦榜 | GET | `/` | `index.html` | 顯示推薦漫畫及熱門排行榜 |
| 搜尋結果 | GET | `/search` | `comic/list.html` | 依關鍵字搜尋漫畫，顯示結果與相似推薦 |
| 分類列表 | GET | `/category/<category_name>` | `comic/list.html` | 依種類（如：熱血、戀愛）顯示漫畫列表 |
| 漫畫詳細資訊 | GET | `/comic/<int:comic_id>` | `comic/detail.html` | 顯示單一漫畫詳細資料與書評列表 |
| 提交書評 | POST | `/comic/<int:comic_id>/review`| — | 接收書評資料，存入 DB 後重導向回詳細頁 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 (`/`)
- **處理邏輯**：
  1. 呼叫 `ComicModel.get_recommended()` 取得推薦清單。
  2. 呼叫 `ComicModel.get_leaderboard()` 取得排行榜。
- **輸出**：渲染 `index.html`。

### 2.2 搜尋與分類列表 (`/search`, `/category/<name>`)
- **輸入**：
  - `/search`: `q` (query string)。
  - `/category/<name>`: URL 參數中的種類名稱。
- **處理邏輯**：
  1. 搜尋：呼叫 `ComicModel.search(q)`。
  2. 分類：呼叫 `ComicModel.get_by_category(name)`。
- **輸出**：渲染 `comic/list.html`。

### 2.3 漫畫詳細資訊 (`/comic/<id>`)
- **輸入**：`comic_id` (URL 參數)。
- **處理邏輯**：
  1. 呼叫 `ComicModel.get_by_id(id)`。
  2. 呼叫 `ReviewModel.get_by_comic_id(id)`。
  3. 呼叫 `ComicModel.get_similar(id)` (搜尋相關漫畫)。
- **輸出**：若找不到則回傳 404，否則渲染 `comic/detail.html`。

### 2.4 提交書評 (`/comic/<id>/review`)
- **輸入**：`nickname`, `content` (POST 表單)。
- **處理邏輯**：
  1. 驗證資料是否完整。
  2. 呼叫 `ReviewModel.create(id, nickname, content)`。
- **輸出**：重導向 (Redirect) 到 `/comic/<id>`。

---

## 3. Jinja2 模板清單

所有模板皆繼承自 `base.html`。

- **`base.html`**: 包含全站導覽列 (包含搜尋框、分類選單) 與頁尾。
- **`index.html`**: 展示首頁大圖推薦、排行榜清單。
- **`comic/list.html`**: 通用的漫畫卡片列表，用於搜尋結果與分類顯示。
- **`comic/detail.html`**: 顯示漫畫大圖、簡介、完結狀態，下方包含書評清單與留言表單。

---

## 4. 路由骨架規劃 (app/routes/)

- **`main.py`**: 包含首頁路由。
- **`comic.py`**: 包含搜尋、分類與詳情路由。
- **`review.py`**: 專門處理書評提交的路由。
