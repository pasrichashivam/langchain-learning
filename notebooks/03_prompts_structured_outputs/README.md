
# Prompt Templates VS Messages

<img src="../../../assets/messages-vs-templates.png" width="800" height="400">

| Approach | Use For |
|----------|---------|
| **Messages** | Agents, dynamic workflows, multi-step reasoning, tool integration |
| **Templates** | Reusable prompts, variable substitution, consistency, RAG systems |

**Both approaches are valuable**: Messages for dynamic workflows, templates for reusability and consistency.

---

### Langchain Templates
```mermaid
graph TD
    A[Templates]
    A --> A1[ChatPromptTemplate]
    A --> A2[PromptTemplate]
    A --> A3[FewShotChatMessagePromptTemplate]
    A --> A4[Template Composition]

```

---

### Few-Shot Prompting with Templates
Teach the AI by providing examples, One of the most powerful prompting techniques.

<img src="../../../assets/few-shot-prompting.png" width="800" height="400">

---

### Template Composition
Build complex prompts by combining smaller templates together.
1. **Base Instructions**: Define common elements used across templates
2. **Specialized Templates**: Add specific instructions for each use case
3. **Compose**: Combine base + specialized + user input

---
---

# Structured Outputs (Pydantic)
Use Pydantic models to get type-safe, structured data from LLMs. This ensures you get exactly the data structure you need.

<img src="../../../assets/structured-output1.png" width="800" height="400">

### Example structured outputs like a form:

- Define the fields (name, email, age)
- The AI fills in the form
- You get validated, typed data back

---

### Steps to get structured LLM response
1. **Define Schema**: Create a Pydantic BaseModel with typed fields
2. **Add Descriptions**: Use Field(description="...") to guide the AI
3. **Create Structured Model**: Call model.with_structured_output(Schema)
4. **Get Typed Data**: Result is a Pydantic model instance with typed attributes

---

### Complex Pydantic Schemas
Build more sophisticated schemas with nested objects, enums, and validation. 

* **Nested Models:** e.g. define Address Model and use it inside Company Model (same like nested Json)
* **Literal Types**: Use Literal["A", "B", "C"] for enum-like constraints
* **Validation**: Pydantic validates types automatically
* **Access Nested Data**: Use dot notation like `result.headquarters.city`

---

## Summary

```mermaid
graph TD
    A[Prompts & Messages] --> B[Messages]
    A --> C[Templates]
    A --> D[Structured Output]
    
    B --> B1[SystemMessage]
    B --> B2[HumanMessage]
    B --> B3[AIMessage]
    B --> B4[ToolMessage]
    
    C --> C1[ChatPromptTemplate]
    C --> C2[PromptTemplate]
    C --> C3[FewShotChatMessagePromptTemplate]
    C --> C4[Template Composition]
    
    D --> D1[Pydantic BaseModel]
    D --> D2[Field Descriptions]
    D --> D3[with_structured_output]
    D --> D4[Nested Schemas]
    
    B4 --> E[Agents]
    C4 --> F[RAG Systems]
```