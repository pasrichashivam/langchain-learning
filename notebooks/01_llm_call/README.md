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

--- 

### Calling model using Openrouter provider 
* Free model usage information by openrouter.
* Openrouter routing system that analyzes prompt and chooses the model that is expected to give the best results
    * Task type
    * Complexity
    * Reasoning required
    * Coding vs Writing vs Math
    * Context length