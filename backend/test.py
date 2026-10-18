import time
from llm import chat, embed

t = time.time()
print(chat("Kısa ve Türkçe cevap ver.", "Fırat Üniversitesi hangi şehirde?"))
print("Chat süresi:", round(time.time() - t, 1), "sn")

t = time.time()
v = embed(["devamsızlık sınırı kaç gün?", "yemekhane menüsü"])
print("Embedding şekli:", v.shape, "süre:", round(time.time() - t, 1), "sn")
