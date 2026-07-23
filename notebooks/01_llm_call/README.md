## LLM Call using Langchain
Using lanchain call models from different providers like OpenAI, Azure, Anthropic with minimal code changes

### Overview

* Initialize and call chat models via LangChain
    1. Single Call
    2. Batch Call
* A look inside the Response returned with LLM call.
    | Field | What it holds |
    |---|---|
    | `.text` | The plain text reply, always be a string |
    | `.content` | The raw content — usually the same as `.text` |
    | `.content_blocks` | Rrepresents rich content (text, reasoning, citations, images) |
    | `.tool_calls` | A list of any tool calls the model requested |
    | `.id` | A unique identifier for returned message |
    | `.usage_metadata` | Token counts for call: input tokens, output tokens, total |
    | `.response_metadata` | Provider-specific information, e.g. which exact model responded and why it stopped generating |
* List of model providers in Langchain Framework
* Single and Batch LLM calls.
* Look into model parameters

---

*Use `init_chat_model()` with a string in the format `"provider:model"`, and everything after that works identically regardless of the provider.*

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
```

**Single-call:** 

* model.invoke("...") returns an AIMessage-like response with `.content`, `.content_blocks`, `.id`, `.usage_metadata`, etc.
* A look into full AI response in Json format.

**Batch calls:**

- model.batch([...]) for parallel execution.
- model.batch_as_completed([...]) to stream results as they complete.
- `config` can control `max_concurrency`.

---

### Model Parameters

| Parameter | Typical Values | Purpose | When to Use |
|-----------|---------------|---------|-------------|
| `model` | `"gpt-5"`, `"gpt-5-mini"` | Selects the LLM | Always required |
| `temperature` | `0.0 – 2.0` | Controls randomness | Lower for deterministic tasks, higher for creativity |
| `max_tokens` | `1` to model limit | Maximum tokens to generate | Control output length and cost |
| `frequency_penalty` | `-2.0 – 2.0` | Discourages/Penalize repeating the same words. | Long-form generation like Blogs|
| `presence_penalty` | `-2.0 – 2.0` | Encourages new topics | Brainstorming |
| `seed` | Integer | Makes output more reproducible | Testing / Evaluation |
| `stop` | List of strings | Stops generation on specified sequences | Structured outputs |
| `timeout` | Seconds | Request timeout | Production |
| `max_retries` | Integer | Retry failed requests | Reliability |
| `streaming` | `True` / `False` | Stream tokens as generated | Chat UI |
| `callbacks` | Callback handlers | Logging & tracing | LangSmith |
| `response_format` | JSON, Text | Structured output | APIs |
| `tools` | List of tools/functions | Function calling | Agents |
--- 

### Calling model using Openrouter provider 
* Free model usage information by openrouter.
* Openrouter routing system that analyzes prompt and chooses the model that is expected to give the best results
    * Task type
    * Complexity
    * Reasoning required
    * Coding vs Writing vs Math
    * Context length