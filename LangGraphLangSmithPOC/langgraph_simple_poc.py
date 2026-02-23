import os
import time
from dotenv import load_dotenv
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Configure LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "langgraph-simple-poc2")

print("🔧 LangSmith Tracing Enabled!")
print(f"📁 Project: {os.environ['LANGCHAIN_PROJECT']}\n")

# Define the state structure
class WorkflowState(TypedDict):
    input: str
    current_step: str
    step_count: int
    results: list
    route: str

# ==================== NODES ====================

def node_start(state: WorkflowState) -> WorkflowState:
    """Entry node - initializes the workflow"""
    print("📍 NODE: START")
    print(f"   Input: {state['input']}")
    
    time.sleep(0.5)  # Simulate processing
    
    return {
        **state,
        "current_step": "start",
        "step_count": state.get("step_count", 0) + 1,
        "results": state.get("results", []) + ["Started workflow"]
    }

def node_analyze(state: WorkflowState) -> WorkflowState:
    """Analyzes the input"""
    print("📍 NODE: ANALYZE")
    print(f"   Analyzing: {state['input']}")
    
    time.sleep(0.5)  # Simulate processing
    
    # Simple routing logic based on input
    if "urgent" in state['input'].lower():
        route = "urgent"
    else:
        route = "normal"
    
    return {
        **state,
        "current_step": "analyze",
        "step_count": state["step_count"] + 1,
        "results": state["results"] + [f"Analyzed input, route: {route}"],
        "route": route
    }

def node_process_urgent(state: WorkflowState) -> WorkflowState:
    """Handles urgent requests"""
    print("📍 NODE: PROCESS URGENT")
    print(f"   Processing urgently...")
    
    time.sleep(0.5)  # Simulate processing
    
    return {
        **state,
        "current_step": "process_urgent",
        "step_count": state["step_count"] + 1,
        "results": state["results"] + ["Processed as URGENT priority"]
    }

def node_process_normal(state: WorkflowState) -> WorkflowState:
    """Handles normal requests"""
    print("📍 NODE: PROCESS NORMAL")
    print(f"   Processing normally...")
    
    time.sleep(0.5)  # Simulate processing
    
    return {
        **state,
        "current_step": "process_normal",
        "step_count": state["step_count"] + 1,
        "results": state["results"] + ["Processed as NORMAL priority"]
    }

def node_validate(state: WorkflowState) -> WorkflowState:
    """Validates the results"""
    print("📍 NODE: VALIDATE")
    print(f"   Validating results...")
    
    time.sleep(0.5)  # Simulate processing
    
    return {
        **state,
        "current_step": "validate",
        "step_count": state["step_count"] + 1,
        "results": state["results"] + ["Validation complete"]
    }

def node_end(state: WorkflowState) -> WorkflowState:
    """Final node - summarizes the workflow"""
    print("📍 NODE: END")
    print(f"   Total steps executed: {state['step_count'] + 1}")
    
    return {
        **state,
        "current_step": "end",
        "step_count": state["step_count"] + 1,
        "results": state["results"] + ["Workflow completed successfully"]
    }

# ==================== CONDITIONAL ROUTING ====================

def route_after_analyze(state: WorkflowState) -> Literal["urgent", "normal"]:
    """Routes based on analysis"""
    route = state.get("route", "normal")
    print(f"🔀 ROUTING: Going to {route.upper()} path")
    return route

def should_validate(state: WorkflowState) -> Literal["validate", "end"]:
    """Decides whether to validate"""
    # Simple logic: validate if step count is less than 5
    if state["step_count"] < 5:
        print(f"🔀 ROUTING: Going to VALIDATE")
        return "validate"
    else:
        print(f"🔀 ROUTING: Skipping validation, going to END")
        return "end"

# ==================== BUILD GRAPH ====================

def create_workflow():
    """Creates and compiles the LangGraph workflow"""
    
    # Initialize the graph with our state type
    workflow = StateGraph(WorkflowState)
    
    # Add all nodes
    workflow.add_node("start", node_start)
    workflow.add_node("analyze", node_analyze)
    workflow.add_node("process_urgent", node_process_urgent)
    workflow.add_node("process_normal", node_process_normal)
    workflow.add_node("validate", node_validate)
    workflow.add_node("end", node_end)
    
    # Set the entry point
    workflow.set_entry_point("start")
    
    # Add edges
    workflow.add_edge("start", "analyze")
    
    # Conditional routing after analyze
    workflow.add_conditional_edges(
        "analyze",
        route_after_analyze,
        {
            "urgent": "process_urgent",
            "normal": "process_normal"
        }
    )
    
    # Both processing paths go to validate decision
    workflow.add_conditional_edges(
        "process_urgent",
        should_validate,
        {
            "validate": "validate",
            "end": "end"
        }
    )
    
    workflow.add_conditional_edges(
        "process_normal",
        should_validate,
        {
            "validate": "validate",
            "end": "end"
        }
    )
    
    # Validate always goes to end
    workflow.add_edge("validate", "end")
    
    # End node goes to END
    workflow.add_edge("end", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

# ==================== MAIN EXECUTION ====================

def print_results(result: WorkflowState):
    """Pretty print the results"""
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(f"Input: {result['input']}")
    print(f"Total Steps: {result['step_count']}")
    print(f"Final Step: {result['current_step']}")
    print(f"\nExecution History:")
    for i, step in enumerate(result['results'], 1):
        print(f"  {i}. {step}")
    print("=" * 60)

def main():
    print("=" * 60)
    print("🚀 LangGraph + LangSmith Simple POC")
    print("=" * 60)
    print("This POC demonstrates:")
    print("  ✓ Node execution")
    print("  ✓ State management")
    print("  ✓ Conditional routing")
    print("  ✓ LangSmith tracing")
    print("=" * 60)
    
    # Create the workflow
    app = create_workflow()
    
    # ===== TEST CASE 1: Normal Request =====
    print("\n" + "🧪 TEST CASE 1: Normal Request")
    print("-" * 60)
    
    initial_state_1 = {
        "input": "Process this normal request",
        "current_step": "",
        "step_count": 0,
        "results": [],
        "route": ""
    }
    
    result_1 = app.invoke(initial_state_1)
    print_results(result_1)
    
    # ===== TEST CASE 2: Urgent Request =====
    print("\n" + "🧪 TEST CASE 2: Urgent Request")
    print("-" * 60)
    
    initial_state_2 = {
        "input": "This is an URGENT request!",
        "current_step": "",
        "step_count": 0,
        "results": [],
        "route": ""
    }
    
    result_2 = app.invoke(initial_state_2)
    print_results(result_2)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n🔍 View detailed traces in LangSmith:")
    print("   https://smith.langchain.com/")
    print(f"   Project: {os.environ['LANGCHAIN_PROJECT']}")
    print("=" * 60)
    
if __name__ == "__main__":
    main()