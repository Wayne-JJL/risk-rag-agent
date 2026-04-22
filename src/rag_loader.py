"""
读取知识文档，并切成块
"""

import os


BASE_DIR = os.path.dirname(__file__)
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "data", "knowledge")


def read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_text_into_chunks(text: str, source_name: str, chunk_size: int = 220, overlap: int = 40):
    chunks = []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunk_id = 1

    for para in paragraphs:
        if len(para) <= chunk_size:
            chunks.append({
                "source": source_name,
                "chunk_id": chunk_id,
                "content": para
            })
            chunk_id += 1
        else:
            start = 0
            while start < len(para):
                end = start + chunk_size
                piece = para[start:end].strip()
                if piece:
                    chunks.append({
                        "source": source_name,
                        "chunk_id": chunk_id,
                        "content": piece
                    })
                    chunk_id += 1
                start += chunk_size - overlap

    return chunks


def load_all_chunks(chunk_size: int = 220, overlap: int = 40):
    all_chunks = []

    if not os.path.exists(KNOWLEDGE_DIR):
        return all_chunks

    for filename in os.listdir(KNOWLEDGE_DIR):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(KNOWLEDGE_DIR, filename)
        text = read_text_file(file_path)
        chunks = split_text_into_chunks(
            text=text,
            source_name=filename,
            chunk_size=chunk_size,
            overlap=overlap
        )
        all_chunks.extend(chunks)

    return all_chunks