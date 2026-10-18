import os, requests, numpy as np

OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemma4:12b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")


def chat(system, user, temperature=0.2, json_mode=False, max_tokens=300):
    body = {
        "model": CHAT_MODEL,
        "stream": False,
        "think": False,
        "keep_alive": "60m",
        "options": {"temperature": temperature, "num_predict": max_tokens},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if json_mode:
        body["format"] = "json"
    r = requests.post(f"{OLLAMA}/api/chat", json=body, timeout=300)
    r.raise_for_status()
    return r.json()["message"]["content"]


def embed(texts):
    r = requests.post(
        f"{OLLAMA}/api/embed",
        json={"model": EMBED_MODEL, "input": texts, "keep_alive": "60m"},
        timeout=300,
    )
    r.raise_for_status()
    v = np.array(r.json()["embeddings"], dtype="float32")
    return v / np.linalg.norm(v, axis=1, keepdims=True)
