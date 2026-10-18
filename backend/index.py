import json
import hashlib
import os
import numpy as np
from llm import embed

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


class Index:
    def __init__(self, items, text_of):
        self.items = items
        if not items:
            self.vecs = np.zeros((0, 1024), dtype="float32")
            return

        texts = [text_of(x) for x in items]
        content_hash = hashlib.md5("###".join(texts).encode("utf-8")).hexdigest()
        cache_path = os.path.join(CACHE_DIR, f"idx_{content_hash}.npy")

        if os.path.exists(cache_path):
            try:
                self.vecs = np.load(cache_path)
            except Exception:
                self.vecs = embed(texts)
                np.save(cache_path, self.vecs)
        else:
            self.vecs = embed(texts)
            try:
                np.save(cache_path, self.vecs)
            except Exception:
                pass

    def search(self, query, k=3):
        if not self.items:
            return []
        q = embed([query])[0]
        scores = self.vecs @ q
        k = min(k, len(self.items))
        top = np.argsort(-scores)[:k]
        return [{**self.items[i], "score": float(scores[i])} for i in top]
