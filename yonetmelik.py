import re, json

text = open("yonetmelik_1.txt", encoding="utf-8").read()
parcalar = re.split(r"\n(?=MADDE\s+\d+\s*[–-])", text)

kayitlar = []
for p in parcalar:
    m = re.match(r"MADDE\s+(\d+)", p)
    if m:
        kayitlar.append({
            "yonetmelik": "Önlisans ve Lisans Eğitim-Öğretim ve Sınav Yönetmeliği",
            "madde_no": int(m.group(1)),
            "baslik": "",
            "metin": p.strip(),
            "kaynak_url": "https://..."
        })

json.dump(kayitlar, open("yonetmelik.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)