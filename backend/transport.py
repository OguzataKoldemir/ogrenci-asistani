from llm import chat
from index import Index, load

HEDEF = "Fırat Üniversitesi"
rotalar = load("data/ulasim.json")
idx = Index(rotalar, lambda r: r["yurt"]) if rotalar else None
ESIK = 0.5
YOK = "Bu güzergah için bilgim yok. Belediye ulaşım birimine danışın."
ANAHTAR = ("fırat", "firat", "üniversite", "universite", "kampüs", "kampus", "okul")


def yurt_listesi():
    return {"yurtlar": [r["yurt"] for r in rotalar]}


def route(yurt, nereye=""):
    if idx is None or not yurt.strip():
        return {"known": False, "answer": YOK, "route": None}
    n = nereye.replace("İ", "i").replace("I", "ı").lower()
    if n.strip() and not any(a in n for a in ANAHTAR):
        return {
            "known": False,
            "answer": "Şu an yalnızca yurtlardan " + HEDEF + "'ne ulaşım bilgisi var. " + YOK,
            "route": None,
        }
    h = idx.search(yurt, k=1)[0]
    if h["score"] < ESIK:
        return {"known": False, "answer": YOK, "route": None}
    ozet = (
        "Yurt: " + h["yurt"] + ", Hedef: " + HEDEF + ", Durak: " + h["durak"]
        + ", Hat: " + h["hat"] + ", Aktarma: " + h["aktarma"]
        + ", Tahmini süre: " + str(h["sure_dk"]) + " dakika"
    )
    try:
        ans = chat(
            "Verilen ulaşım bilgisini öğrenciye en fazla 2 kısa cümleyle, Türkçe anlat. "
            "Hat için 'numaralı hat' de, araç türü verilmediyse otobüs veya minibüs deme. "
            "Aktarma 'Yok' ise aktarmasız olduğunu söyle. SADECE verilen bilgiyi kullan, bilgi uydurma.",
            ozet,
            max_tokens=150,
        )
    except Exception:
        ans = ozet
    return {"known": True, "answer": ans, "route": h}
