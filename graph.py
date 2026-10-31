from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Step 1: Define the state schema
class ExpenseState(TypedDict):
    total: float
    answer: str


# Step 2: Create actual input state
state: ExpenseState = {
    "total": 1200.0,
    "answer": ""
}


# Step 3: Create a node function
def calculate_expenses(state: ExpenseState):
    total = state["total"]
    print(total)
    return {"total": total}


# Step 4: Create the graph builder
builder = StateGraph(ExpenseState)


# Step 5: Add the node
builder.add_node("calculate-expenses", calculate_expenses)


# Step 6: Connect START to the node
builder.add_edge(START, "calculate-expenses")


# Step 7: Connect the node to END
builder.add_edge("calculate-expenses", END)


# Step 8: Compile the graph
graph = builder.compile()


# Step 9: Execute the graph
result = graph.invoke(state)


# Step 10: Print the final result
print(result)


#graph
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))