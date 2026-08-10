from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from rich import print

def pretty_print_messages(state):
    """Pretty-print a LangChain agent state."""
    messages = state.get("messages", [])

    for i, msg in enumerate(messages, 1):
        print("=" * 80)
        print(f"Message {i}")

        if isinstance(msg, HumanMessage):
            print("Role : Human")
        elif isinstance(msg, AIMessage):
            print("Role : AI")
        elif isinstance(msg, ToolMessage):
            print("Role : Tool")
        elif isinstance(msg, SystemMessage):
            print("Role : System")
        else:
            print(f"Role : {type(msg).__name__}")

        print("-" * 80)
        print(msg.content)

        if isinstance(msg, AIMessage) and msg.tool_calls:
            print("\nTool Calls:")
            for tool in msg.tool_calls:
                print(f"  • Name : {tool['name']}")
                print(f"    Args : {tool['args']}")
                print(f"    ID   : {tool['id']}")

        if isinstance(msg, ToolMessage):
            print(f"\nTool Name : {msg.name}")
            print(f"Tool Call : {msg.tool_call_id}")

    print("=" * 80)

def print_messages(result):
    for m in result['messages']:
        if isinstance(m, HumanMessage):
            print(f"[bold green]HumanMessage:[/bold green] {m.content}")
        elif isinstance(m, AIMessage):
            if m.tool_calls:
                print(f"[bold yellow]Agent:[/bold yellow] AIMessage with tool calls:")
                for i, tool_call in enumerate(m.tool_calls, start=1):
                    print(f"[bold yellow]Tool Call {i} Name:[/bold yellow] {tool_call['name']}\n[bold yellow]Tool Call {i} Args:[/bold yellow] {tool_call['args']}")
            else:
                print(f"[bold yellow]Agent:[/bold yellow] {m.content}")
        elif isinstance(m, ToolMessage):
            print(f"[bold cyan]ToolMessage:[/bold cyan] {m.content}")
        print("=" * 80)