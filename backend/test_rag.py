import time
import rag

sorular = [
    "Devamsızlık sınırı nedir?",
    "Çift anadal başvurusu için not ortalaması kaç olmalı?",
    "Yaz okulunda en fazla kaç ders alabilirim?",
    "Yatay geçiş için başvuru şartları nelerdir?",
    "Pizza nasıl yapılır?",
]
for s in sorular:
    t = time.time()
    hits = rag.idx.search(s, k=1)
    print("SORU:", s)
    print("  en yüksek skor:", round(hits[0]["score"], 3), "|", hits[0]["kaynak"][:35], hits[0]["madde"])
    r = rag.ask(s)
    print("  known:", r["known"])
    print("  cevap:", r["answer"])
    print("  süre:", round(time.time() - t, 1), "sn")
    print()
