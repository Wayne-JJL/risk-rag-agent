from llm_client import chat_completion
from prompts import CLASSIFIER_PROMPT


def keyword_classify(user_input: str):
    text = user_input.lower()

    metric_keywords = ["auc", "ks", "psi", "逾期率", "坏账率", "通过率", "拒绝率"]
    rule_keywords = [
        "缺失率", "分布漂移", "一致性", "数据质量", "排查", "规则",
        "异常", "怎么办", "怎么定位", "怎么排查", "如何排查",
        "如何定位", "如何处理", "先看什么", "上线后", "报表未更新",
        "etl", "同步失败", "延迟", "链路"
    ]

    # 先判断 rule：排查 / 异常 / 处理类问题优先归到 rule
    for k in rule_keywords:
        if k in text:
            return "rule", f"命中 rule 关键词: {k}"

    # 再判断 metric：仅当是纯指标解释或定义类问题时才归到 metric
    for k in metric_keywords:
        if k in text:
            return "metric", f"命中 metric 关键词: {k}"

    # “指标”这个词本身不要直接强判 metric
    # 因为“指标异常怎么办”本质上更像 rule
    if "指标" in text:
        if any(x in text for x in ["是什么", "怎么计算", "定义", "含义", "什么意思"]):
            return "metric", "命中 metric 语义模式: 指标定义/计算"
        if any(x in text for x in ["异常", "怎么办", "怎么排查", "怎么定位", "先看什么"]):
            return "rule", "命中 rule 语义模式: 指标异常排查"

    return "unknown", "未命中关键词规则"


def llm_classify(user_input: str):
    messages = [
        {"role": "system", "content": CLASSIFIER_PROMPT},
        {"role": "user", "content": user_input}
    ]

    result = chat_completion(messages, temperature=0)
    label = result["content"].strip().lower()

    if label not in ["metric", "rule", "chat"]:
        return "chat", "LLM 分类结果异常，回退为 chat"

    return label, "通过 LLM 分类得到结果"


def classify_task(user_input: str):
    label, reason = keyword_classify(user_input)

    if label != "unknown":
        return label, reason

    return llm_classify(user_input)