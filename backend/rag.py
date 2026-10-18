from llm import chat
from index import Index, load

maddeler = load("data/yonetmelik.json")
idx = Index(maddeler, lambda m: m["kaynak"] + " " + m["madde"] + ": " + m["metin"])

ESIK = 0.40
BILMIYORUM = "Bilmiyorum, bu konuda öğrenci işleri birimine danışın."

SYSTEM = (
    "Sen Fırat Üniversitesi öğrenci asistanısın. "
    "SADECE verilen madde metinlerine dayanarak Türkçe ve kısa cevap ver. "
    "Cevapta kullandığın maddenin numarasını ve kaynağını belirt. "
    "Metinlerde cevap yoksa sadece şunu yaz: BILMIYORUM"
)


def ask(question):
    hits = idx.search(question, k=3)
    if hits[0]["score"] < ESIK:
        return {"known": False, "answer": BILMIYORUM, "sources": []}
    context = "\n\n".join(
        "[" + h["kaynak"] + " - " + h["madde"] + "]\n" + h["metin"] for h in hits
    )
    out = chat(SYSTEM, "MADDELER:\n" + context + "\n\nSORU: " + question)
    if "BILMIYORUM" in out:
        return {"known": False, "answer": BILMIYORUM, "sources": hits}
    return {"known": True, "answer": out, "sources": hits}
