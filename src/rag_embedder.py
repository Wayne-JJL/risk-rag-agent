from sentence_transformers import SentenceTransformer

# 第一次运行会自动下载模型
_model = SentenceTransformer("BAAI/bge-small-zh-v1.5")


def get_embedding(text: str):
    vec = _model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def get_embeddings(text_list: list[str]):
    vectors = _model.encode(text_list, normalize_embeddings=True)
    return [vec.tolist() for vec in vectors]