import json
import os
"""
保存和读取切块、向量
"""

BASE_DIR = os.path.dirname(__file__)
STORE_DIR = os.path.join(BASE_DIR, "data", "rag_store")
CHUNKS_PATH = os.path.join(STORE_DIR, "chunks.json")
VECTORS_PATH = os.path.join(STORE_DIR, "vectors.json")


def ensure_store_dir():
    os.makedirs(STORE_DIR, exist_ok=True)


def save_chunks(chunks: list):
    ensure_store_dir()
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def save_vectors(vectors: list):
    ensure_store_dir()
    with open(VECTORS_PATH, "w", encoding="utf-8") as f:
        json.dump(vectors, f)


def load_chunks():
    if not os.path.exists(CHUNKS_PATH):
        return []
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_vectors():
    if not os.path.exists(VECTORS_PATH):
        return []
    with open(VECTORS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)