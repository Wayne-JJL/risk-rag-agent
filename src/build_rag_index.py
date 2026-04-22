from rag_loader import load_all_chunks
from rag_embedder import get_embeddings
from rag_store import save_chunks, save_vectors
"""
构建知识库
"""

def main():
    print("开始加载知识文档并切块...")
    chunks = load_all_chunks(chunk_size=220, overlap=40)
    print(f"共生成 {len(chunks)} 个 chunks")

    texts = [chunk["content"] for chunk in chunks]

    print("开始生成 embeddings...")
    vectors = get_embeddings(texts)
    print(f"共生成 {len(vectors)} 个向量")

    save_chunks(chunks)
    save_vectors(vectors)

    print("RAG 索引构建完成。")


if __name__ == "__main__":
    main()