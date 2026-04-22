from router import classify_task
from tools import (
    get_metric_info,
    format_metric_tool_result,
    search_rule,
    extract_metric_names,
    extract_rule_keyword
)
from prompts import build_answer_messages
from llm_client import chat_completion
from memory import add_message, trim_history
from utils import (
    compress_assistant_message,
    is_unsupported_request,
    build_unsupported_answer,
    is_identity_request,
    build_identity_answer,
    has_no_rule_evidence
)


def is_action_request(user_input: str) -> bool:
    keywords = [
        "怎么排查", "怎么定位", "怎么办", "如何处理",
        "先看什么", "如何排查", "如何定位", "怎么解决"
    ]
    return any(k in user_input for k in keywords)


def run_agent(user_input, history, max_turns=3):
    unsupported, unsupported_reason = is_unsupported_request(user_input)
    if unsupported:
        answer = build_unsupported_answer(user_input)
        add_message(history, "user", user_input)
        add_message(history, "assistant", compress_assistant_message(answer))
        history = trim_history(history, max_turns=max_turns)

        return {
            "task_type": "unsupported",
            "route_reason": unsupported_reason,
            "tool_name": "none",
            "tool_result": "",
            "citations": [],
            "answer": answer,
            "usage": None,
            "history": history
        }

    identity_request, identity_reason = is_identity_request(user_input)
    if identity_request:
        answer = build_identity_answer()
        add_message(history, "user", user_input)
        add_message(history, "assistant", compress_assistant_message(answer))
        history = trim_history(history, max_turns=max_turns)

        return {
            "task_type": "identity",
            "route_reason": identity_reason,
            "tool_name": "none",
            "tool_result": "",
            "citations": [],
            "answer": answer,
            "usage": None,
            "history": history
        }

    task_type, route_reason = classify_task(user_input)

    tool_name = "none"
    tool_result = ""
    citations = []
    mode = "chat"
    answer_style = "normal"

    # ========= metric 分支：恢复 LLM 主答，但必须基于证据 =========
    if task_type == "metric":
        metric_names = extract_metric_names(user_input)
        tool_name = "explain_metric"

        if not metric_names:
            answer = (
                "我当前没有在指标库中识别到这个指标。"
                "你可以先把这个指标补充进 metrics.json，"
                "或者告诉我你想让我按‘定义、计算方式、业务意义’哪种结构来整理。"
            )

            add_message(history, "user", user_input)
            add_message(history, "assistant", compress_assistant_message(answer))
            history = trim_history(history, max_turns=max_turns)

            return {
                "task_type": task_type,
                "route_reason": route_reason,
                "tool_name": tool_name,
                "tool_result": "未识别到具体指标名称。",
                "citations": [],
                "answer": answer,
                "usage": None,
                "history": history
            }

        metric_infos = []
        for name in metric_names:
            info = get_metric_info(name)
            if info:
                metric_infos.append(info)

        if not metric_infos:
            answer = (
                "我当前没有在指标库中识别到这个指标。"
                "你可以先把这个指标补充进 metrics.json，"
                "或者告诉我你想让我按‘定义、计算方式、业务意义’哪种结构来整理。"
            )

            add_message(history, "user", user_input)
            add_message(history, "assistant", compress_assistant_message(answer))
            history = trim_history(history, max_turns=max_turns)

            return {
                "task_type": task_type,
                "route_reason": route_reason,
                "tool_name": tool_name,
                "tool_result": "未识别到具体指标名称。",
                "citations": [],
                "answer": answer,
                "usage": None,
                "history": history
            }

        tool_result = format_metric_tool_result(metric_infos)
        mode = "metric_tool"

        messages = build_answer_messages(
            history=history,
            user_input=user_input,
            tool_context=tool_result,
            mode=mode,
            answer_style="normal",
            citations=None
        )

        result = chat_completion(messages, temperature=0.3)
        answer = result["content"]
        usage = result["usage"]

        add_message(history, "user", user_input)
        add_message(history, "assistant", compress_assistant_message(answer))
        history = trim_history(history, max_turns=max_turns)

        return {
            "task_type": task_type,
            "route_reason": route_reason,
            "tool_name": tool_name,
            "tool_result": tool_result,
            "citations": [],
            "answer": answer,
            "usage": usage,
            "history": history
        }

    # ========= rule 分支：保持 RAG + 引用 =========
    elif task_type == "rule":
        keyword = extract_rule_keyword(user_input)
        tool_name = "search_rag_knowledge"

        search_result = search_rule(keyword, top_k=2)
        tool_result = search_result["tool_result"]
        citations = search_result["citations"]

        if has_no_rule_evidence(tool_result):
            answer = (
                "我当前没有在本地知识文档中检索到相关内容。"
                "你可以把这类规则补充到 knowledge 文档里，"
                "我再基于新文档帮你回答。"
            )

            add_message(history, "user", user_input)
            add_message(history, "assistant", compress_assistant_message(answer))
            history = trim_history(history, max_turns=max_turns)

            return {
                "task_type": task_type,
                "route_reason": route_reason,
                "tool_name": tool_name,
                "tool_result": tool_result,
                "citations": citations,
                "answer": answer,
                "usage": None,
                "history": history
            }

        mode = "rule_tool"

        if is_action_request(user_input):
            answer_style = "action_first"

        messages = build_answer_messages(
            history=history,
            user_input=user_input,
            tool_context=tool_result,
            mode=mode,
            answer_style=answer_style,
            citations=citations
        )

        result = chat_completion(messages, temperature=0.3)
        answer = result["content"]
        usage = result["usage"]

        add_message(history, "user", user_input)
        add_message(history, "assistant", compress_assistant_message(answer))
        history = trim_history(history, max_turns=max_turns)

        return {
            "task_type": task_type,
            "route_reason": route_reason,
            "tool_name": tool_name,
            "tool_result": tool_result,
            "citations": citations,
            "answer": answer,
            "usage": usage,
            "history": history
        }

    # ========= chat 分支 =========
    messages = build_answer_messages(
        history=history,
        user_input=user_input,
        tool_context="",
        mode="chat",
        answer_style="normal",
        citations=None
    )

    result = chat_completion(messages, temperature=0.3)
    answer = result["content"]
    usage = result["usage"]

    add_message(history, "user", user_input)
    add_message(history, "assistant", compress_assistant_message(answer))
    history = trim_history(history, max_turns=max_turns)

    return {
        "task_type": task_type,
        "route_reason": route_reason,
        "tool_name": "none",
        "tool_result": "",
        "citations": [],
        "answer": answer,
        "usage": usage,
        "history": history
    }