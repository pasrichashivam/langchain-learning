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

def pretty_print_agent_output(result):
    """Pretty-print a LangGraph/LangChain agent result."""
    print("🤖 AGENT OUTPUT")
    print("=" * 70)

    # Messages
    for msg in result.get("messages", []):
        msg_type = type(msg).__name__

        if msg_type == "HumanMessage":
            print(f"\n👤 User:")
            print(f"   {msg.content}")

        elif msg_type == "AIMessage":
            print(f"\n🤖 Assistant:")

            if msg.content:
                print(f"   {msg.content}")

            # Tool calls
            for tool_call in getattr(msg, "tool_calls", []):
                print(f"\n🔧 Tool Call:")
                print(f"   Name : {tool_call['name']}")
                print(f"   Args : {tool_call['args']}")
                print(f"   ID   : {tool_call['id']}")

    # Interrupt / Human approval
    interrupts = result.get("__interrupt__", [])

    if interrupts:
        print("\n" + "-" * 70)
        print("⏸️  HUMAN APPROVAL REQUIRED")
        print("-" * 70)

        for interrupt in interrupts:
            value = interrupt.value

            for action in value.get("action_requests", []):
                print(f"\n⚠️  Action: {action['name']}")
                print(f"   Args       : {action['args']}")
                print(f"   Description: {action['description']}")

            for config in value.get("review_configs", []):
                print(f"\n📋 Allowed decisions:")
                print(f"   {', '.join(config['allowed_decisions'])}")

            print(f"\n   Interrupt ID: {interrupt.id}")

    print("\n" + "=" * 70)