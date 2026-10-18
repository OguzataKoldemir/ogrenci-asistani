import json, datetime, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import rag, advisor, clubs, transport

app = FastAPI(title="Fırat Öğrenci Asistanı API")

# CORS middleware for local development and LAN access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Q(BaseModel):
    question: str


class Idea(BaseModel):
    idea: str


class ClubReq(BaseModel):
    interests: list[str] = []
    text: str = ""


@app.get("/health")
def health():
    return {"ok": True, "service": "Fırat Asistan Backend", "status": "active"}


@app.post("/api/ask")
def ask(b: Q):
    return rag.ask(b.question)


@app.post("/api/advisor")
def adv(b: Idea):
    return advisor.advise(b.idea)


@app.post("/api/clubs")
def cl(b: ClubReq):
    return clubs.recommend(b.interests, b.text)


@app.get("/api/menu/today")
def menu_today():
    gun = datetime.date.today().isoformat()
    data = {}
    menu_path = os.path.join(os.path.dirname(__file__), "data", "menu.json")
    if os.path.exists(menu_path):
        try:
            with open(menu_path, encoding="utf-8-sig") as f:
                data = json.load(f)
        except Exception:
            data = {}

    if isinstance(data, dict) and gun in data:
        return {"tarih": gun, "var": True, **data[gun]}
    return {
        "tarih": gun,
        "var": False,
        "ogle": [
            "Ezogelin Çorbası",
            "Fırın Tavuk & Patates",
            "Pirinç Pilavı",
            "Mevsim Salata"
        ],
        "aksam": [
            "Mercimek Çorbası",
            "Kıymalı Bezelye",
            "Bulgur Pilavı",
            "Yoğurt / Meyve"
        ],
        "mesaj": "Bugünkü örnek menü listelenmektedir (Güncel duyuru SKS sayfasında).",
    }


@app.get("/api/transport/yurtlar")
def yurtlar():
    return transport.yurt_listesi()


@app.get("/api/transport")
def trans(yurt: str = "", nereye: str = ""):
    return transport.route(yurt, nereye)


# Frontend static files mounting (must be at the end)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "firat-asistan"))
if os.path.isdir(FRONTEND_DIR):
    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
