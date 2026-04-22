import json
import os

from rag_retriever import retrieve_top_k


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


METRICS_DB = load_json("metrics.json")


def get_metric_info(metric_name: str):
    metric_name = metric_name.strip()

    if metric_name in METRICS_DB:
        item = METRICS_DB[metric_name]
        return {
            "metric": metric_name,
            "definition": item["definition"],
            "reason": item["common_issues"],
            "advice": item["advice"]
        }

    return None


def format_metric_tool_result(metric_infos: list[dict]) -> str:
    parts = []

    for item in metric_infos:
        parts.append(
            f"指标：{item['metric']}\n"
            f"定义：{item['definition']}\n"
            f"异常原因：{item['reason']}\n"
            f"建议：{item['advice']}"
        )

    return "\n\n".join(parts)


def search_rule(query: str, top_k: int = 2) -> dict:
    results = retrieve_top_k(query, top_k=top_k)

    if not results:
        return {
            "tool_result": "没有在本地 RAG 知识库中检索到相关内容。",
            "citations": [],
            "raw_results": []
        }

    parts = []
    citations = []

    for idx, item in enumerate(results, start=1):
        citation = f"{item['source']}#{item['chunk_id']}"
        citations.append(citation)

        parts.append(
            f"检索片段 {idx}\n"
            f"来源：{citation}\n"
            f"相似度分数：{item['score']}\n"
            f"内容：{item['content']}"
        )

    return {
        "tool_result": "\n\n".join(parts),
        "citations": citations,
        "raw_results": results
    }


def extract_metric_names(user_input: str) -> list:
    text_upper = user_input.upper()
    matched = []

    for metric in METRICS_DB.keys():
        if metric.isascii():
            if metric.upper() in text_upper:
                matched.append(metric)
        else:
            if metric in user_input:
                matched.append(metric)

    return matched


def extract_rule_keyword(user_input: str) -> str:
    return user_input.strip()