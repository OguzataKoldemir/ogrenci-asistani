import json

with open("data/yonetmelik1.json", encoding="utf-8-sig") as f:
    ham = json.load(f)

gorulen = set()
out = []
for r in ham:
    anahtar = (r["yonetmelik"], r["madde_no"], r["metin"])
    if anahtar in gorulen:
        continue
    gorulen.add(anahtar)
    satirlar = [s.strip() for s in r["metin"].split("\n") if s.strip()]
    parcalar, simdiki = [], ""
    for s in satirlar:
        if simdiki and len(simdiki) + len(s) > 1000:
            parcalar.append(simdiki)
            simdiki = s
        else:
            simdiki = (simdiki + " " + s).strip()
    if simdiki:
        parcalar.append(simdiki)
    for i, p in enumerate(parcalar):
        madde = "Madde " + str(r["madde_no"])
        if len(parcalar) > 1:
            madde += " (parça " + str(i + 1) + "/" + str(len(parcalar)) + ")"
        out.append({
            "kaynak": r["yonetmelik"],
            "madde": madde,
            "metin": p,
            "url": r["kaynak_url"],
        })

with open("data/yonetmelik.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("ham kayıt:", len(ham), "-> benzersiz parça:", len(out))
