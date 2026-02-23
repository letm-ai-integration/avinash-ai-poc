# 🌐 LangChain MCP POC Application (uv + Python)

This Proof of Concept (POC) demonstrates a modular AI application built using **LangChain**, a **custom MCP (Model Context Protocol) server & client architecture**, and managed with **uv** (Python package manager).

The system consists of:

* 🧠 A **custom MCP client**
* 🌤️ A **Weather MCP Server** (weather search tool)
* ➗ A **Math MCP Server** (math operations toolset)
* ⚡ Built and managed using **uv**
* 🐍 Implemented in **Python**

---

## 📌 Architecture Overview

```
User
  ↓
Custom MCP Client (LangChain Agent)
  ↓
---------------------------------------
|             MCP Servers             |
|-------------------------------------|
| 1. Weather Server  → Weather Tool  |
| 2. Math Server     → Math Tools    |
---------------------------------------
```

### Components

#### 🔹 Custom MCP Client

* Built using LangChain
* Connects to multiple MCP servers
* Routes tool calls dynamically
* Handles reasoning and tool invocation

#### 🔹 Weather MCP Server

Provides:

* `get_weather(location: str)`
* Returns real weather data

#### 🔹 Math MCP Server

Provides:

* `add(a, b)`
* `multiply(a, b)`

---

## 🛠 Tech Stack

* **Python 3.10+**
* **LangChain**
* **MCP (Model Context Protocol)**
* **uv** (fast Python package manager)
* Async architecture

---

# 🚀 Setup Instructions

## 1️⃣ Install uv

If not installed:

```bash
pip install uv
```

or

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2️⃣ Create Virtual Environment

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

---

## 3️⃣ Install Dependencies

```bash
uv pip install -r requirements.txt
```

Example `requirements.txt`:

```
langchain
mcp
fastapi
uvicorn
pydantic
```

---

# ▶️ Running the Application

## Start Weather MCP Server

```bash
python servers/weather_server.py
```

Runs on:

```
http://localhost:8001
```

---

## Start Math MCP Server

```bash
python servers/math_server.py
```

Runs on:

```
http://localhost:8002
```

---

## Start Custom MCP Client

```bash
python client/main.py
```

---

# 🧪 Example Usage

### Weather Query

```
User: What’s the weather in New York?
```

Flow:

1. LangChain agent identifies weather intent
2. Calls Weather MCP server
3. Returns structured weather response

---

### Math Query

```
User: What is 25 multiplied by 4?
```

Flow:

1. Agent detects math intent
2. Calls Math MCP server
3. Returns computed result

---

# 🔎 How It Works

### 1️⃣ LangChain Agent

* Uses tool calling capabilities
* Registers MCP tools dynamically
* Handles reasoning before tool invocation

### 2️⃣ MCP Communication

* Client communicates with servers over HTTP
* Servers expose tools via MCP interface
* JSON-based request/response cycle

### 3️⃣ Tool Execution

* Weather tool fetches/mock weather data
* Math tool performs arithmetic operations
* Results returned to client → formatted → user response

---
