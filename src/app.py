from prompts import AGENT_SYSTEM_PROMPT
from memory import init_history
from agent import run_agent
from utils import print_usage


def main():
    print("=== Agent V1.3.2 启动成功 ===")
    print("输入 quit 退出程序。\n")

    history = init_history(AGENT_SYSTEM_PROMPT)

    while True:
        user_input = input("你：").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("已退出。")
            break

        try:
            result = run_agent(user_input=user_input, history=history, max_turns=3)
            history = result["history"]

            print(f"\n[任务类型] {result['task_type']}")
            print(f"[路由原因] {result['route_reason']}")
            print(f"[使用工具] {result['tool_name']}")

            if result["tool_result"]:
                print(f"[工具结果]\n{result['tool_result']}\n")

            print(f"助手：{result['answer']}\n")
            print_usage(result["usage"])
            print("-" * 50)

        except Exception as e:
            print(f"发生错误：{e}")
            print("请稍后重试。")
            print("-" * 50)


if __name__ == "__main__":
    main()