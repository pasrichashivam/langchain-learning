# Multi-Agent Patterns in LangChain
* Multi-agent systems coordinate specialized components to tackle complex workflows. 

## Why multi-agent?
* Multi-agents are used for one or more of these capabilities:
    * **Context management**: 
        * Provide specialized knowledge without overwhelming the model’s context window. 
        * If context were infinite and latency zero, you could dump all knowledge into a single prompt
        * **Context Isolation** helps to provide task specific context to sub agents to selectively surface relevant information.
    * **Distributed development:** Allow different teams to develop and maintain capabilities independently, composing them into a larger system with clear boundaries.
    * **Parallelization**: Spawn specialized workers for subtasks and execute them concurrently for faster results.

## Patterns
Here are the main patterns for building multi-agent systems, each suited to different use cases:

| Pattern | How it works |
| --- | --- |
| Subagents | A main agent coordinates subagents as tools. All routing passes through the main agent, which decides when and how to invoke each subagent. |
| Handoffs | Behavior changes dynamically based on state. Tool calls update a state variable that triggers routing or configuration changes, switching agents or adjusting the current agent’s tools and prompt. |
| Skills | Specialized prompts and knowledge loaded on-demand. A single agent stays in control while loading context from skills as needed. |
| Router | A routing step classifies input and directs it to one or more specialized agents. Results are synthesized into a combined response. |
| Custom workflow | Build bespoke execution flows with LangGraph, mixing deterministic logic and agentic behavior. Embed other patterns as nodes in your workflow. |

## Choosing a pattern

* **Distributed development**: Can different teams maintain components independently?
* **Parallelization**: Can multiple agents execute concurrently?
* **Multi-hop**: Does the pattern support calling multiple subagents in series?
* **Direct user interaction**: Can subagents converse directly with the user?

### A quick distinction: Subagents vs. Handoffs vs. Router

These three are the ones most often confused with each other, so it's worth being precise
about what separates them:

- **Subagents**: the *supervisor* is itself a full agent. It decides, turn by turn, which
  sub-agent-as-tool to call, and can call several in sequence or in parallel. The sub-agents
  don't talk to the user directly.
- **Handoffs**: there's no supervisor doing live reasoning about where to route. Instead, state
  (such as `current_step`, or which agent is "active") determines which prompt and tools are in
  effect right now. Agents can hand off to each other, or a single agent can reconfigure itself.
- **Router**: a *classification step* (often one structured-output LLM call, not a full agent)
  decides, once, which specialized agents are relevant, dispatches to all of them **in
  parallel**, and a synthesis step combines their answers. There's no multi-turn orchestration.

### 1. Subagents
* A **supervisor** agent coordinates both, deciding which tool to call for a given request and combining their results into one coherent answer. 
* We'll also add **human-in-the-loop review**
so a person can approve, edit, or reject sensitive actions (like an outbound email) before
they actually happen.

```mermaid
graph LR
    U([User request]) --> SV[Supervisor agent]
    SV -->|schedule_event tool| CA[Calendar agent]
    SV -->|manage_email tool| EA[Email agent]
    CA -->|create_calendar_event| C1[(Calendar API)]
    CA -->|get_available_time_slots| C1
    EA -->|send_email| C2[(Email API)]
    CA -.response.-> SV
    EA -.response.-> SV
    SV --> R([Combined answer])
```
#### Why a supervisor, instead of one agent with every tool?
* Give one agent direct access to both calendar and email APIs, and it has to choose from similar-looking tools, understand each API's exact format, and juggle two unrelated domains in one prompt. 
* Splitting the work into two focused specialists, each with its own tools and prompt, keeps each one simple and makes each one independently testable.

### 2. Handoffs
* In the handoffs architecture, behavior changes dynamically based on state.
* Unlike Subagents, where a supervisor calls separate agents as tools, the **state machine pattern** uses a **single agent** whose configuration (system prompt + tools) changes dynamically based on where the conversation is. 
```mermaid
flowchart LR
    Start([Customer reports an issue]) --> Warranty{Is the device under warranty?}
    Warranty -->|Yes| IssueType{What type of issue?}
    Warranty -->|No| OutOfWarranty{What type of issue?}
    IssueType -->|Hardware| Repair[Provide warranty repair instructions]
    IssueType -->|Software| Troubleshoot[Provide troubleshooting steps]
    OutOfWarranty -->|Hardware| Escalate[Escalate to human for paid repair]
    OutOfWarranty -->|Software| Troubleshoot
    Troubleshoot --> Close([Issue resolved])
    Repair --> Close
    Escalate --> Close

    classDef startEnd fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef decisionNode fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef actionNode fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    classDef escalateNode fill:#F8E8E6,stroke:#B27D75,stroke-width:2px,color:#634643
    class Start,Close startEnd
    class Warranty,IssueType,OutOfWarranty decisionNode
    class Repair,Troubleshoot actionNode
    class Escalate escalateNode
```
### 3. Router
* In the router architecture, a routing step classifies input and directs it to specialized agents.
* This is useful when you have distinct verticals (separate knowledge domains that each require their own agent).
```mermaid
graph LR
    A([Query]) --> B[Classify]
    B --> C[GitHub agent]
    B --> D[Notion agent]
    B --> E[Slack agent]
    C --> F[Synthesize]
    D --> F
    E --> F
    F --> G([Combined answer])

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    class A,G trigger
    class B,C,D,E,F process
```

### 4. Skills
* In the skills architecture, specialized capabilities are packaged as invocable “skills” that augment an agent’s behavior.
* Skills are primarily prompt-driven specializations that an agent can invoke on-demand
* This uses **progressive disclosure** loading information on demand instead of upfront 
* To Implement **skills**: specialized, prompt-based instructions the agent loads via tool calls or middlewares.

```mermaid
flowchart LR
    Start([User: Write SQL query<br/>for high-value customers]) --> SystemPrompt[Agent sees skill descriptions:<br/>sales_analytics, inventory_management]
    SystemPrompt --> Decide{Need sales schema}
    Decide --> LoadSkill[load_skill'sales_analytics']
    LoadSkill --> Schema[Schema loaded:<br/>customers, orders tables<br/>+ business logic]
    Schema --> WriteQuery[Agent writes SQL query<br/>using schema knowledge]
    WriteQuery --> Response([Returns valid SQL<br/>following business rules])

    classDef startEnd fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    classDef decision fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef enrichment fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
    class Start,Response startEnd
    class SystemPrompt,LoadSkill,WriteQuery process
    class Decide decision
    class Schema enrichment
```

## Performance comparison


## Useful Resources for Learning MultiAgents
* [**MultiAgent System**](https://ai-automation-with-mayank.netlify.app/#agents)