from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, json, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"status": "ok", "message": "DubaiElite API"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/properties")
def properties():
    conn = get_db()
    rows = conn.execute("SELECT * FROM realty_objects WHERE status='ACTIVE' LIMIT 20").fetchall()
    data = [dict(r) for r in rows]
    conn.close()
    return {"success": True, "data": data}

@app.get("/api/translations/{lang}")
def translations(lang: str = "en"):
    t = {
        "en": {"btn_search": "Search", "btn_create": "Create", "btn_matches": "Matches", "btn_my_listings": "My", "btn_analytics": "Stats"},
        "ru": {"btn_search": "Поиск", "btn_create": "Создать", "btn_matches": "Мэтчи", "btn_my_listings": "Мои", "btn_analytics": "Аналитика"},
        "ar": {"btn_search": "بحث", "btn_create": "إنشاء", "btn_matches": "مطابقات", "btn_my_listings": "قوائمي", "btn_analytics": "تحليلات"}
    }
    return {"success": True, "data": t.get(lang, t["en"])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
