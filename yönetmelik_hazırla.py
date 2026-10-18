import re, json, sys, pathlib
from io import BytesIO
from html.parser import HTMLParser
import requests
from pypdf import PdfReader

# Yeni yönetmelik eklemek için sadece buraya satır ekle
KAYNAKLAR = [
    {
        "id": "yatay_gecis",
        "ad": "Önlisans ve Lisans Eğitim-Öğretim Yatay Geçiş Yönetmeliği",
        "url": "https://www.firat.edu.tr/documents/1695379863.pdf",
        "tip": "pdf",   # "pdf" veya "html"
    },{
            "id": "egitim_ogretim",
                "ad": "Önlisans ve Lisans Eğitim-Öğretim ve Sınav Yönetmeliği",
                "url": "https://www.firat.edu.tr/documents/1686567516.pdf",
                "tip": "pdf",
    },{"id": "yaz_okulu",
            "ad": "Yaz Okulu Yönetmeliği",
            "url": "https://ftr.firat.edu.tr/documentFiles/1737547077717.FIRAT%20UNIVERSITY%20SUMMER%20SCHOOL%20REGULATIONS.pdf",
            "tip": "pdf",},{
                "id": "Çift Anadal Yönetmeliği",
                    "ad": "Önlisans ve Lisans Eğitim-Öğretim ve Sınav Yönetmeliği",
                    "url": "https://www.firat.edu.tr/documents/1686567516.pdf",
                    "tip": "pdf",},
                    
                    {"id": "cift_anadal",
                            "ad": "Çift Anadal ve Yandal Yönetmeliği",
                            "url": "https://www.firat.edu.tr/documents/1733993859.pdf",
                            "tip": "pdf",}
    # {"id": "yatay_gecis", "ad": "...", "url": "...", "tip": "pdf"},
]

RAW = pathlib.Path("raw")
RAW.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0"}


class MetinAyiklayici(HTMLParser):
    """HTML içindeki görünür metni standart kütüphaneyle çıkarır."""

    def __init__(self):
        super().__init__()
        self.parcalar = []
        self.gizli = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.gizli += 1
        elif tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3"):
            self.parcalar.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.gizli:
            self.gizli -= 1
        elif tag in ("p", "div", "li", "tr", "h1", "h2", "h3"):
            self.parcalar.append("\n")

    def handle_data(self, data):
        if not self.gizli:
            self.parcalar.append(data)


def metni_getir(k, yenile=False):
    txt_yolu = RAW / f"{k['id']}.txt"
    # Elle düzelttiğin txt dosyası varsa ÜZERİNE YAZMAZ
    if txt_yolu.exists() and not yenile:
        print(f"[cache] {k['id']} (elle düzeltmen korunuyor)")
        return txt_yolu.read_text(encoding="utf-8")

    print(f"[indir] {k['id']}")
    r = requests.get(k["url"], headers=HEADERS, timeout=30)
    r.raise_for_status()

    if k["tip"] == "pdf":
        okuyucu = PdfReader(BytesIO(r.content))
        metin = "\n".join((s.extract_text() or "") for s in okuyucu.pages)
    else:
        ayiklayici = MetinAyiklayici()
        ayiklayici.feed(r.text)
        metin = "".join(ayiklayici.parcalar)

    txt_yolu.write_text(metin, encoding="utf-8")
    return metin


def maddelere_bol(metin, k):
    desen = re.compile(r"(?im)^\s*MADDE\s+(\d+)\s*[–\-—]")
    eslesmeler = list(desen.finditer(metin))
    kayitlar = []
    for i, m in enumerate(eslesmeler):
        bas = m.start()
        son = eslesmeler[i + 1].start() if i + 1 < len(eslesmeler) else len(metin)
        kayitlar.append({
            "yonetmelik": k["ad"],
            "madde_no": int(m.group(1)),
            "baslik": "",
            "metin": metin[bas:son].strip(),
            "kaynak_url": k["url"],
        })
    return kayitlar


if __name__ == "__main__":
    yenile = "--yenile" in sys.argv
    hepsi = []
    for k in KAYNAKLAR:
        try:
            metin = metni_getir(k, yenile)
            maddeler = maddelere_bol(metin, k)
            print(f"  -> {len(maddeler)} madde bulundu")
            hepsi.extend(maddeler)
        except Exception as e:
            print(f"[HATA] {k['id']}: {e}")

    pathlib.Path("data").mkdir(exist_ok=True)
    with open("data/yonetmelik.json", "w", encoding="utf-8") as f:
        json.dump(hepsi, f, ensure_ascii=False, indent=2)
    print(f"Toplam {len(hepsi)} madde -> data/yonetmelik.json")