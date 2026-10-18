import json
from llm import chat
from index import Index, load

UNVANLAR = ["Prof. Dr.", "Doç. Dr.", "Dr. Öğr. Üyesi", "Arş. Gör.", "Öğr. Gör."]


def tr_title(s):
    out = []
    for w in s.split():
        low = w.replace("İ", "i").replace("I", "ı").lower()
        f = low[0]
        f = "İ" if f == "i" else "I" if f == "ı" else f.upper()
        out.append(f + low[1:])
    return " ".join(out)


def kisa_unvan(u):
    for x in UNVANLAR:
        if x in u:
            return x
    return u


def hazirla(h):
    h = dict(h)
    h["ad"] = tr_title(h["ad"])
    h["unvan"] = kisa_unvan(h["unvan"])
    h["alanlar"] = h.get("alanlar") or []
    h["yayinlar"] = h.get("yayinlar") or []
    return h


hocalar = [hazirla(h) for h in load("data/hocalar.json")]


def hoca_metni(h):
    t = h["bolum"]
    if h["alanlar"]:
        t += ". Alanlar: " + ", ".join(h["alanlar"])
    if h["yayinlar"]:
        t += ". Yayınlar: " + "; ".join(h["yayinlar"])
    return t


idx = Index(hocalar, hoca_metni)


def bilgi(h):
    s = h["unvan"] + " " + h["ad"] + " - bölüm: " + h["bolum"]
    if h["alanlar"]:
        s += " - alanlar: " + ", ".join(h["alanlar"])
    if h["yayinlar"]:
        s += " - yayınlar: " + "; ".join(h["yayinlar"])
    if not h["alanlar"] and not h["yayinlar"]:
        s += " (alan ve yayın bilgisi yok, sadece bölüm bilgisi var)"
    return s


def advise(idea):
    hits = idx.search(idea, k=3)
    ozet = "\n".join(str(i + 1) + ". " + bilgi(h) for i, h in enumerate(hits))
    raw = chat(
        "Öğrencinin proje fikri ile akademisyenlerin bölümünü, alanlarını ve yayınlarını karşılaştır. "
        "Her akademisyen için 1-2 cümlelik Türkçe gerekçe yaz. "
        "SADECE verilen bilgiye dayan. Alan veya yayın bilgisi yoksa yayın ya da uzmanlık uydurma, "
        "sadece bölümünün fikirle ilgisini söyle. "
        'Sadece şu JSON biçiminde cevap ver: {"gerekceler": ["...", "...", "..."]}',
        "FİKİR: " + idea + "\n\nAKADEMİSYENLER:\n" + ozet,
        json_mode=True,
        max_tokens=500,
    )
    try:
        g = json.loads(raw)["gerekceler"]
    except Exception:
        g = []
    for i, h in enumerate(hits):
        h["gerekce"] = g[i] if i < len(g) else ""
    top = hits[0]
    detay = "\nHocanın ilgili yayını: " + top["yayinlar"][0] if top["yayinlar"] else ""
    mail = chat(
        "Kısa, kibar ve resmi bir Türkçe e-posta taslağı yaz. Konu satırı ekle. "
        "Sadece verilen bilgileri kullan, yayın veya bilgi uydurma. "
        "Öğrenci adı yerine [Ad Soyad] yaz.",
        "Öğrencinin bitirme projesi fikri: " + idea
        + "\nHoca: " + top["unvan"] + " " + top["ad"]
        + "\nBölüm: " + top["bolum"]
        + detay
        + "\nAmaç: proje danışmanlığı için görüşme randevusu istemek.",
        max_tokens=400,
    )
    return {"matches": hits, "email_draft": mail}
