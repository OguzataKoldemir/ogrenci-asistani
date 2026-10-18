import json, re, glob

def temizle(x):
    if isinstance(x, str):
        return re.sub(r"\s*\[cite[^\]]*\]", "", x).strip()
    if isinstance(x, list):
        return [temizle(i) for i in x]
    if isinstance(x, dict):
        return {k: temizle(v) for k, v in x.items()}
    return x

for p in glob.glob("data/*.json"):
    with open(p, encoding="utf-8-sig") as f:
        d = json.load(f)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(temizle(d), f, ensure_ascii=False, indent=1)
    print("temizlendi:", p)
