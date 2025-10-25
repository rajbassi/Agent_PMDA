# Agentic AI Assignment 6 - Math Agent System

A sophisticated AI agent system that solves mathematical equations using a multi-component architecture with perception, decision-making, and action execution capabilities.

## 🏗️ Architecture Overview

This project implements an **agentic AI system** with four core components:

1. **Perception** (`perception.py`) - Analyzes and understands mathematical problems
2. **Decision** (`decide.py`) - Plans the step-by-step solution approach
3. **Action** (`action.py`) - Executes mathematical operations using MCP tools
4. **Memory** (`memory.py`) - Stores and retrieves context and state

## 🚀 Features

- **Interactive Math Solving**: Solves complex mathematical equations with step-by-step reasoning
- **MCP Tool Integration**: Uses Model Context Protocol for mathematical operations
- **Async/Await Architecture**: High-performance asynchronous processing
- **Memory Management**: Persistent context storage for multi-step problem solving
- **Timeout Handling**: Robust error handling with configurable timeouts
- **Iterative Problem Solving**: Breaks down complex problems into manageable steps

## 📋 Prerequisites

- Python 3.13+
- Google Gemini API key
- Windows OS (for pywinauto dependency)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Assignment6
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or using uv (recommended)
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   MODEL=gemini-2.0-flash
   ```

## 🏃‍♂️ Quick Start

1. **Run the main application**:
   ```bash
   python main.py
   ```

2. **Follow the interactive prompts**:
   - Enter a mathematical equation (e.g., `5+((2+3)*(4+6))/2`)
   - Specify output format preferences
   - Watch the agent solve the problem step-by-step

## 📁 Project Structure

```
Assignment6/
├── main.py              # Main application entry point
├── perception.py         # Problem analysis and understanding
├── decide.py            # Decision-making and planning
├── action.py            # Action execution and tool calling
├── memory.py            # Memory management system
├── models.py            # Pydantic data models
├── mcp_server.py        # MCP server with math tools
├── pyproject.toml       # Project dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

## 🔧 Core Components

### 1. Perception Module (`perception.py`)
- **Purpose**: Analyzes mathematical problems and generates solution strategies
- **Key Function**: `get_query_perception()` - Creates step-by-step solution plans
- **Features**: 
  - Tool-aware problem analysis
  - Strategy generation for complex equations
  - Timeout-protected LLM calls

### 2. Decision Module (`decide.py`)
- **Purpose**: Plans the next action in the solution process
- **Key Function**: `decide_next_step()` - Determines what operation to perform next
- **Features**:
  - Iterative decision making
  - Tool selection and parameter preparation
  - Response parsing and validation

### 3. Action Module (`action.py`)
- **Purpose**: Executes mathematical operations using MCP tools
- **Key Function**: `call_tools()` - Calls specific mathematical functions
- **Features**:
  - MCP server communication
  - Tool execution with error handling
  - Result processing and formatting

### 4. Memory Module (`memory.py`)
- **Purpose**: Stores and retrieves context information
- **Key Functions**:
  - `store(key, value)` - Store information
  - `recall(key)` - Retrieve information
  - `clear()` - Reset memory

### 5. MCP Server (`mcp_server.py`)
- **Purpose**: Provides mathematical operation tools
- **Available Tools**:
  - `add(a, b)` - Addition
  - `subtract(a, b)` - Subtraction
  - `multiply(a, b)` - Multiplication
  - `divide(a, b)` - Division
  - `add_list(numbers)` - Sum of list

## 🔄 Workflow

1. **Input**: User provides mathematical equation and preferences
2. **Perception**: System analyzes the problem and creates a solution strategy
3. **Memory**: Store the context and user preferences
4. **Iteration Loop**:
   - **Decision**: Determine next mathematical operation
   - **Action**: Execute the operation using MCP tools
   - **Repeat**: Continue until equation is solved
5. **Output**: Present final answer with complete solution steps

## 🎯 Example Usage

```python
# Example equation: 5+((2+3)*(4+6))/2
# Expected solution steps:
# 1. Calculate (2+3) = 5
# 2. Calculate (4+6) = 10  
# 3. Calculate 5*10 = 50
# 4. Calculate 50/2 = 25
# 5. Calculate 5+25 = 30
# Final Answer: 30
```

## ⚙️ Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `MODEL`: Model to use (default: "gemini-2.0-flash")

### System Prompt
The system uses a carefully crafted prompt that instructs the AI to:
- Use available tools for calculations
- Follow specific response formats
- Provide step-by-step solutions
- Handle complex nested expressions

## 🛡️ Error Handling

- **Timeout Protection**: All LLM calls have configurable timeouts
- **Tool Execution Errors**: Graceful handling of mathematical errors
- **Connection Issues**: Robust MCP server communication
- **Invalid Input**: Input validation and sanitization

## 📊 Dependencies

- `google-genai>=1.45.0` - Google Gemini AI integration
- `mcp[cli]>=1.18.0` - Model Context Protocol
- `pillow>=12.0.0` - Image processing
- `pywinauto>=0.6.9` - Windows automation
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management

## 🚨 Troubleshooting

### Common Issues

1. **API Key Not Found**:
   - Ensure `.env` file exists with `GEMINI_API_KEY`
   - Check API key validity

2. **MCP Server Connection Failed**:
   - Verify `mcp_server.py` is accessible
   - Check Python path configuration

3. **Timeout Errors**:
   - Increase timeout values in configuration
   - Check network connectivity

4. **Tool Execution Errors**:
   - Verify mathematical expression syntax
   - Check for division by zero

## 🔮 Future Enhancements

- [ ] Support for more complex mathematical functions
- [ ] Graphical equation input
- [ ] Step-by-step visualization
- [ ] Multiple solution strategies
- [ ] Integration with external math libraries
- [ ] Web interface for equation solving

## 📝 License

This project is part of an academic assignment for Agentic AI coursework.

## 🤝 Contributing

This is an academic project. For questions or issues, please contact the course instructor.

---

**Note**: This system requires a valid Google Gemini API key and is designed for educational purposes in understanding agentic AI architectures.
