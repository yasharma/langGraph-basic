# LangGraph Basics - AI Chatbot with Web Search

A conversational AI chatbot built with LangGraph that can search the web using Tavily to provide up-to-date information and answers.

## Features

- 🤖 **Intelligent Conversation**: Powered by OpenAI's GPT-4 for natural language understanding
- 🔍 **Web Search Integration**: Uses Tavily Search API to find current information
- 🔄 **Dynamic Tool Usage**: Automatically decides when to search for information vs. responding directly
- 📊 **Interactive Jupyter Notebook**: Explore and visualize the chatbot's workflow
- 🎯 **State Management**: Maintains conversation context using LangGraph's state system

## Project Structure

```
langGraph-basics/
├── main.py              # Main chatbot application with CLI interface
├── chatbot.ipynb        # Jupyter notebook for interactive exploration
├── chatbot.py           # (Currently empty - for future extensions)
├── util/
│   ├── __init__.py      # Package initialization
│   └── State.py         # State management for conversation messages
└── README.md            # This file
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Tavily API key

## Installation

1. **Clone or download the project**:
   ```bash
   cd langGraph-basics
   ```

2. **Install required packages**:
   ```bash
   pip install langgraph langchain langchain-openai langchain-tavily python-dotenv
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

   You can get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Tavily: https://tavily.com/

## Usage

### Command Line Interface

Run the main chatbot application:

```bash
python main.py
```

The chatbot will start an interactive session where you can:
- Ask questions that require web search (e.g., "What's the latest news about AI?")
- Have general conversations
- Type `quit`, `exit`, or `q` to end the session

### Jupyter Notebook

For interactive exploration and visualization:

```bash
jupyter notebook chatbot.ipynb
```

The notebook includes:
- Graph visualization of the chatbot workflow
- Step-by-step execution of the conversation flow
- Interactive testing environment

## How It Works

The chatbot uses a **state graph** architecture:

1. **Start** → User input is received
2. **Chatbot Node** → GPT-4 processes the message and decides:
   - If web search is needed → Routes to Tools
   - If direct response is sufficient → Routes to End
3. **Tools Node** → Executes Tavily search when needed
4. **Loop Back** → Returns to Chatbot with search results
5. **End** → Provides final response to user

### State Management

The `State` class maintains conversation context:
- **Messages**: List of all conversation messages (user + assistant)
- **Add Messages**: Appends new messages while preserving history

### Tools Integration

- **Tavily Search**: Configured to return top 2 most relevant results
- **Automatic Tool Binding**: GPT-4 automatically decides when to use search
- **Conditional Routing**: Graph intelligently routes between conversation and search

## Configuration

### Customizing the Model

In `main.py`, you can change the LLM model:
```python
llm = init_chat_model("openai:gpt-4o")  # Use GPT-4o instead
llm = init_chat_model("anthropic:claude-3-sonnet")  # Use Claude
```

### Adjusting Search Results

Modify the number of search results:
```python
tool = TavilySearch(max_results=5)  # Get more results
```

### Adding More Tools

Extend the tools list in `main.py`:
```python
from langchain_community.tools import WikipediaQueryRun
wiki_tool = WikipediaQueryRun()
tools = [tool, wiki_tool]
```

## Example Conversations

**Web Search Example**:
```
User: What's the current stock price of Apple?
Assistant: [Searches web] Apple (AAPL) is currently trading at $185.42...
```

**Direct Response Example**:
```
User: What is 2 + 2?
Assistant: 2 + 2 equals 4.
```

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure `.env` file is in the project root
   - Check that API keys are valid and have sufficient credits

2. **Import Errors**:
   - Install all required packages: `pip install -r requirements.txt`
   - Ensure you're using Python 3.8+

3. **Connection Issues**:
   - Check internet connection for API calls
   - Verify API endpoints are accessible

### Debug Mode

For detailed logging, add to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Feel free to extend this project by:
- Adding new tools and integrations
- Improving the conversation flow
- Creating additional specialized agents
- Enhancing the user interface

## License

This project is open source and available under the MIT License.

## Resources

- [LangGraph Documentation](https://langraph-langchain.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Tavily API Documentation](https://docs.tavily.com/)