from dotenv import load_dotenv

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

from util.State import State
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from db import db
from rich.console import Console
from rich.panel import Panel
console = Console()

load_dotenv()

# Memory Saver
# This is used to save the state of the conversation, so that it can be resumed later
# You can use any other memory saver, like Redis, or a database
memory = MemorySaver()



llm = init_chat_model("openai:gpt-4.1")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

sql_tools = toolkit.get_tools()

# Extract the tools we need
tavily_tool = TavilySearch(max_results=2)
schema_tool = next(tool for tool in sql_tools if tool.name == "sql_db_schema")
query_tool = next(tool for tool in sql_tools if tool.name == "sql_db_query")

# All tools - now the LLM can choose between web search and database operations
tools = [tavily_tool, schema_tool, query_tool]

graph_builder = StateGraph(State)
tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)

# Bind all tools to LLM
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "2"}}
# ...existing imports and setup...

def stream_graph_updates(user_input: str):
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    for event in events:
        message = event["messages"][-1]

        # Check if message has tool calls
        if hasattr(message, 'tool_calls') and message.tool_calls:
            # Display tool usage
            for tool_call in message.tool_calls:
                console.print(f"[yellow]🔧 Using tool:[/yellow] {tool_call.get('name', 'unknown')}")
        
        # Enhanced display with Rich console
        if hasattr(message, 'content') and message.content:
            console.print(Panel(
                message.content,
                title="🤖 Assistant",
                title_align="left",
                border_style="blue",
                padding=(1, 2)
            ))
        elif hasattr(message, 'tool_calls'):
            console.print("[dim]🔄 Processing tool calls...[/dim]")

# Enhanced main loop
console.print(Panel(
    "🤖 LangGraph Chatbot with Database & Web Search\n\n" +
    "💬 Ask me anything!\n" +
    "📊 Database queries: 'How many users?', 'Show me artists'\n" +
    "🌐 Web search: 'Latest news', 'Current weather'\n" +
    "❌ Type 'quit', 'exit', or 'q' to end",
    title="Welcome",
    border_style="cyan"
))

while True:
    try:
        user_input = console.input("\n[bold green]User:[/bold green] ")
        if user_input.lower() in ["quit", "exit", "q"]:
            console.print("[bold red]Goodbye![/bold red]")
            break

        stream_graph_updates(user_input)
    except KeyboardInterrupt:
        console.print("\n[bold red]Goodbye![/bold red]")
        break
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        user_input = "What do you know about LangGraph?"
        console.print(f"[bold green]User:[/bold green] {user_input}")
        stream_graph_updates(user_input)
        break