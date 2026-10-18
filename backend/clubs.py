from index import Index, load

kulupler = load("data/kulupler.json")


def kulup_metni(k):
    return k["ad"] + ". Kategori: " + k["kategori"]


idx = Index(kulupler, kulup_metni)


def recommend(interests, text):
    q = ", ".join(interests) + ". " + text
    return {"clubs": idx.search(q, k=5)}
