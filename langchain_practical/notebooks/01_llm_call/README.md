## First LLM Call

*Use `init_chat_model()` with a string in the format `"provider:model"`, and everything after that works identically regardless of the provider.*

```python
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
```
