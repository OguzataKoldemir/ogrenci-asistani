import json
import numpy as np
from llm import embed


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


class Index:
    def __init__(self, items, text_of):
        self.items = items
        self.vecs = embed([text_of(x) for x in items])

    def search(self, query, k=3):
        q = embed([query])[0]
        scores = self.vecs @ q
        top = np.argsort(-scores)[:k]
        return [{**self.items[i], "score": float(scores[i])} for i in top]
