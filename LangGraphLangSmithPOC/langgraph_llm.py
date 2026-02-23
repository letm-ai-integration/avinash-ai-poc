import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

load_dotenv()

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "langgraph_llm"

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # or "llama2-70b-4096"
    temperature=0.7
)

# Define State
class State(TypedDict):
    messages: list
    summary: str
    sentiment: str

# Node 1: Analyze sentiment
def analyze_sentiment(state: State):
    print("📍 NODE: Analyzing Sentiment...")
    
    user_message = state["messages"][-1]
    
    prompt = f"Analyze the sentiment of this message in one word (positive/negative/neutral): '{user_message}'"
    response = llm.invoke(prompt)
    sentiment = response.content.strip().lower()
    
    print(f"   Sentiment: {sentiment}")
    
    return {
        **state,
        "sentiment": sentiment
    }

# Node 2: Generate response
def generate_response(state: State):
    print("📍 NODE: Generating Response...")
    
    user_message = state["messages"][-1]
    sentiment = state["sentiment"]
    
    prompt = f"User said: '{user_message}' (Sentiment: {sentiment}). Write a helpful, friendly response."
    response = llm.invoke(prompt)
    
    print(f"   Response: {response.content[:100]}...")
    
    return {
        **state,
        "messages": state["messages"] + [f"Assistant: {response.content}"]
    }

# Node 3: Summarize
def summarize_conversation(state: State):
    print("📍 NODE: Summarizing...")
    
    conversation = "\n".join(state["messages"])
    
    prompt = f"Summarize this conversation in one sentence:\n{conversation}"
    response = llm.invoke(prompt)
    
    print(f"   Summary: {response.content}")
    
    return {
        **state,
        "summary": response.content
    }

# Build the graph
def create_graph():
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("analyze", analyze_sentiment)
    workflow.add_node("respond", generate_response)
    workflow.add_node("summarize", summarize_conversation)
    
    # Define flow
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "respond")
    workflow.add_edge("respond", "summarize")
    workflow.add_edge("summarize", END)
    
    return workflow.compile()

# Run
def main():
    print("=" * 60)
    print("🚀 LangGraph + Groq + LangSmith POC")
    print("=" * 60)
    
    app = create_graph()
    
    # Test
    initial_state = {
        "messages": ["I'm done with this product!"],
        "summary": "",
        "sentiment": ""
    }
    
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print(f"Sentiment: {result['sentiment']}")
    print(f"Summary: {result['summary']}")
    print("\nFull conversation:")
    for msg in result['messages']:
        print(f"  - {msg}")
    
    print("\n" + "=" * 60)
    print("✅ Check LangSmith: https://smith.langchain.com/")
    print("=" * 60)
    png_data = app.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png_data)

if __name__ == "__main__":
    main()