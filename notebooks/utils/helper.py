from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
                                     
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