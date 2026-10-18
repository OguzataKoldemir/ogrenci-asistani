import json, datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import rag, advisor, clubs, transport

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
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
    return {"ok": True}


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
    with open("data/menu.json", encoding="utf-8-sig") as f:
        data = json.load(f)
    gun = datetime.date.today().isoformat()
    if gun in data:
        return {"tarih": gun, "var": True, **data[gun]}
    return {
        "tarih": gun,
        "var": False,
        "ogle": [],
        "aksam": [],
        "mesaj": "Bugün için menü verisi girilmemiş. Güncel menü için Sağlık Kültür ve Spor Daire Başkanlığı duyurularına bakın.",
    }


@app.get("/api/transport/yurtlar")
def yurtlar():
    return transport.yurt_listesi()


@app.get("/api/transport")
def trans(yurt: str = "", nereye: str = ""):
    return transport.route(yurt, nereye)
