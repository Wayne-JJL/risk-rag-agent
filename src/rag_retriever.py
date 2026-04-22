import numpy as np

from rag_embedder import get_embedding
from rag_store import load_chunks, load_vectors
"""
用户提问时做相似度检索
"""

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    denominator = (np.linalg.norm(v1) * np.linalg.norm(v2))
    if denominator == 0:
        return 0.0

    return float(np.dot(v1, v2) / denominator)


def retrieve_top_k(query: str, top_k: int = 2):
    chunks = load_chunks()
    vectors = load_vectors()

    if not chunks or not vectors:
        return []

    query_vector = get_embedding(query)

    scored = []
    for chunk, vector in zip(chunks, vectors):
        score = cosine_similarity(query_vector, vector)
        item = chunk.copy()
        item["score"] = round(score, 4)
        scored.append(item)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]