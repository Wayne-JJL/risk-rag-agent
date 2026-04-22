"""
负责会话历史和裁剪
"""
def init_history(system_prompt: str):
    return [
        {"role": "system", "content": system_prompt}
    ]

def add_message(history, role, content):
    history.append({"role": role, "content": content})
    return history

def trim_history(history, max_turns=3):
    """
    保留：1）第一条system 2）最近max_turns轮用户/助手对话 3）1轮 = user+assistan两条消息
    """
    if len(history) <= 1:
        return history

    system_message = history[0]
    rest = history[1:]

    keep_num = max_turns * 2
    trimmed = rest[-keep_num:]

    return [system_message] + trimmed