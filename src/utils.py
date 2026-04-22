def print_usage(usage):
    if not usage:
        print("Token 用量：当前接口未返回 usage")
        return

    prompt_tokens = getattr(usage, "prompt_tokens", None)
    completion_tokens = getattr(usage, "completion_tokens", None)
    total_tokens = getattr(usage, "total_tokens", None)

    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Completion Tokens: {completion_tokens}")
    print(f"Total Tokens: {total_tokens}")


def compress_assistant_message(answer: str, max_len=100):
    answer = answer.replace("\n", " ").strip()
    return answer[:max_len]


def is_unsupported_request(user_input: str) -> tuple[bool, str]:
    """
    判断是不是当前版本暂不支持的请求
    """
    text = user_input.lower()

    unsupported_keywords = {
        "weather": ["天气", "气温", "下雨", "晴天", "阴天", "台风"],
        "news": ["新闻", "热点", "热搜", "最近发生了什么"],
        "finance_realtime": ["股价", "汇率", "黄金价格", "比特币价格", "实时行情"],
        "time_sensitive": ["今天", "明天", "现在几点", "实时"]
    }

    for category, keywords in unsupported_keywords.items():
        for kw in keywords:
            if kw in text:
                return True, f"命中暂不支持的 {category} 关键词: {kw}"

    return False, ""


def build_unsupported_answer(user_input: str) -> str:
    return (
        "我当前这个 V1.2 版本主要用于指标解释、规则说明和基础聊天，"
        "暂不支持查询实时天气、新闻、股价、汇率等外部实时信息。"
    )

def is_identity_request(user_input: str) -> tuple[bool, str]:
    text = user_input.lower()

    identity_keywords = [
        "你是谁", "你是干嘛的", "你能做什么", "介绍一下你自己",
        "who are you", "what can you do"
    ]

    for kw in identity_keywords:
        if kw in text:
            return True, f"命中身份类关键词: {kw}"

    return False, ""


def build_identity_answer() -> str:
    return (
        "我是一个本地练习项目里的 Agent V1.2。"
        "当前主要支持三类能力：指标解释、规则说明和基础聊天。"
        "如果是实时天气、新闻、股价、汇率这类外部实时信息，我暂时不支持。"
    )

def has_no_metric_evidence(tool_result: str) -> bool:
    return tool_result.strip().startswith("未识别到具体指标名称") or \
           tool_result.strip().startswith("没有找到指标")


def has_no_rule_evidence(tool_result: str) -> bool:
    return "没有在本地知识文档中检索到相关内容" in tool_result