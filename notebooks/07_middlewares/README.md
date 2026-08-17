# Middlewares In Langchain

<img src="../../assets/middlewares_graph.png" width="500" height="400">

<img src="../../assets/middleware_callbacks.png" width="500" height="400">


| Middleware            | Description                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------- |
| Tool error            | Catch tool execution exceptions and convert them to error messages for the model.             |
| Tool retry            | Automatically retry failed tool calls with exponential backoff.                               |
| Model retry           | Automatically retry failed model calls with exponential backoff.                              |
| Model fallback        | Automatically fallback to alternative models when primary fails.                              |
| Summarization         | Automatically summarize conversation history when approaching token limits.                   |
| Human-in-the-loop     | Pause execution for human approval of tool calls.                                             |
| Model call limit      | Limit the number of model calls to prevent excessive costs.                                   |
| Tool call limit       | Control tool execution by limiting call counts.                                               |
| PII detection         | Detect and handle Personally Identifiable Information (PII).                                  |
| To-do list            | Equip agents with task planning and tracking capabilities.                                    |
| LLM tool selector     | Use an LLM to select relevant tools before calling main model.                                |
| Provider tool search  | Defer tools behind providers’ server-side tool search, surfacing them on demand.              |
| Shell tool            | Expose a persistent shell session to agents for command execution.                            |
| Filesystem            | Provide agents with a filesystem for storing context and long-term memories.                  |
| Subagent              | Add the ability to spawn subagents.                                                           |
| Rubric grading (Beta) | Apply LLM-as-a-judge grading so agents self-evaluate and iterate until a rubric is satisfied. |
| File search           | Provide Glob and Grep search tools over filesystem files.                                     |
| Context editing       | Manage conversation context by trimming or clearing tool uses.                                |
| LLM tool emulator     | Emulate tool execution using an LLM for testing purposes.                                     |


```mermaid
flowchart LR
    A["Request"] --> M1["before model"]
    M1 --> B["Model call"]
    B --> M2["after model"]
    M2 --> C["Tool call"]
    C --> M3["after tool"]
    M3 --> D["Final result"]
```

---

### 1. SummarizationMiddleware

```mermaid
flowchart TD
    A[Conversation grows] --> B{Approaching token limit?}
    B -- No --> C[Continue conversation]
    B -- Yes --> D[Summarization middleware]
    D --> E[Summarize older conversation history]
    E --> F[Replace old history with summary]
    F --> G[Continue with recent messages + summary]
    G --> C
```

```python
    middleware=[
            SummarizationMiddleware(
                model="openai:gpt-5-nano",
                trigger=("tokens", 300),
                keep=("messages", 1),
            )
        ]
```

---

### 2. HumanInTheLoopMiddleware (HITL)

```mermaid
flowchart TD
    A[Agent execution] --> B[Agent decides to call a tool]
    B --> C{Requires human approval?}
    C -- No --> D[Execute tool]
    C -- Yes --> E[Pause execution]
    E --> F[Request human approval]
    F --> G{Approved?}
    G -- Yes --> D[Execute tool]
    G -- No --> H[Reject / modify tool call]
    D --> I[Return tool result to agent]
    H --> I
    I --> J[Continue agent execution]
```

```python
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"cancel_booking": {"allowed_decisions": ["approve", "edit", "reject", "respond"]}},
        ),
    ]
```

### 3. ModelCallLimitMiddleware

```mermaid
flowchart TD
    A[Agent receives request] --> B[ModelCallLimitMiddleware]
    
    B --> C{Before model call:<br/>check call count}
    
    C -->|Count < limit| D[Increment model call count]
    D --> E[Call LLM / Chat Model]
    E --> F[Model returns response]
    
    F --> G{Continue agent loop?}
    
    G -->|Yes| B
    G -->|No| H[Return final response]
    
    C -->|Count >= limit| I{Exceeded limit behavior}
    
    I -->|exit_behavior = end| J[Stop agent execution]
    I -->|exit_behavior = error| K[Raise ModelCallLimitError]
    
    J --> H
    K --> L[Error returned to caller]
```

```python
    middleware=[
        ModelCallLimitMiddleware( 
            thread_limit=5,   
            exit_behavior="end",
        ),
    ]
```

### 4. ModelFallbackMiddleware

flowchart TD
    A[Agent Request] --> B[Primary Model]
    B -->|Success| E[Response]
    B -->|Failure| C[Fallback Model 1]
    C -->|Success| E
    C -->|Failure| D[Fallback Model 2]
    D -->|Success| E
    D -->|Failure| F[Error]

```python
    middleware=[
        ModelFallbackMiddleware(
            "openai:gpt-5-nano"
        ),
    ]
```

