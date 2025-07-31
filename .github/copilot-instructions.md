# LangGraph Chatbot Development Guide

## Architecture Overview

This is a **multi-modal AI chatbot** built with LangGraph that combines:
- **Web search** (Tavily API) for current information
- **Database querying** (SQLite/Chinook.db) via SQL toolkit
- **Conversational AI** with OpenAI GPT-4.1

### Core Components

**State Management**: Uses `util/State.py` with `add_messages` annotation for conversation context
```python
# State automatically appends messages, never overwrites
messages: Annotated[list, add_messages]
```

**Graph Architecture**: Single-node tool routing via `tools_condition`
```python
# LLM automatically chooses between tools based on user intent
tools = [tavily_tool, schema_tool, query_tool, query_checker_tool]
graph_builder.add_conditional_edges("chatbot", tools_condition, {"tools": "tools", END: END})
```

**Database Integration**: Uses `SQLDatabaseToolkit` with Chinook.db (music store schema)
- `sql_db_schema`: Get table structures
- `sql_db_query`: Execute SELECT queries  
- `sql_db_query_checker`: Validate SQL before execution

## Key Patterns

### Tool Registration
Always extract tools from `SQLDatabaseToolkit` with safe fallbacks:
```python
schema_tool = next(tool for tool in sql_tools if tool.name == "sql_db_schema")
query_checker_tool = next((tool for tool in sql_tools if tool.name == "sql_db_query_checker"), None)
```

### Memory Management
Use thread-specific configs for conversation persistence:
```python
config = {"configurable": {"thread_id": "unique_id"}}
graph.stream({"messages": [...]}, config)
```

### Rich Console Output
Use Rich console for enhanced UX with tool call visualization:
```python
# Color-code different tool types
if tool_name == "sql_db_query_checker":
    console.print(f"[red]🔍 Validating query:[/red] {tool_name}")
```

## Development Workflows

### Adding New Tools
1. Extract from toolkit or create custom tool
2. Add to `tools` list (LLM auto-discovers capabilities)
3. Update system message if needed for routing hints

### Database Schema
Current schema: Chinook music store (Artist, Album, Track, Customer, Invoice, etc.)
- Always use `LIMIT` clauses for query safety
- Leverage `sql_db_schema` tool for structure discovery

### Testing Flow
- **CLI**: `python main.py` for interactive testing
- **Notebook**: `chatbot.ipynb` for step-by-step debugging and visualization
- Test both database queries ("How many artists?") and web search ("Latest AI news")

### Environment Setup
Required `.env` keys:
```
OPENAI_API_KEY=sk-proj-...
TAVILY_API_KEY=tvly-dev-...
```

## Common Pitfalls

- **Tool routing**: LLM decides tool usage - avoid complex manual routing
- **Memory persistence**: Always pass same `thread_id` for conversation continuity  
- **SQL safety**: Query checker validates before execution - include in tools list
- **Stream mode**: Use `stream_mode="values"` to get full message events
- **Rich display**: Check `hasattr(message, 'content')` before rendering panels

## Extension Points

- Add custom tools via `langchain.tools.BaseTool`
- Replace `MemorySaver` with Redis/database for production persistence
- Swap database by changing `db.py` connection string
- Customize LLM model via `init_chat_model("provider:model")`

"""
Represents a visualization module for LangGraph. This module provides functionality to create, manage, and render LangGraph visualizations.

LangGraph is a library for building stateful, multi-actor applications with LLMs. This visualization component helps in:
- Rendering graph structures
- Displaying node relationships
- Visualizing state transitions
- Showing execution paths through the graph

The module integrates with the broader LangGraph framework to provide visual representations of graph-based workflows, making it easier to understand and debug complex LLM-powered applications.

For more information about LangGraph, see:
- https://github.com/langchain-ai/langgraph
- https://python.langchain.com/docs/langgraph
"""