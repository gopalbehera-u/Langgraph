from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import StateGraph, START, END, MessagesState

# 1. Initialize LLM
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)

# 2. Create a tool
@tool
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b

# 3. Bind tool to LLM
llm_with_tool = llm.bind_tools([multiply])

# 4. Create ToolNode
tool_node = ToolNode([multiply])

# 5. Create graph builder
builder = StateGraph(MessagesState)

# 6. Create LLM node
def call_llm(state: MessagesState):
    response = llm_with_tool.invoke(state["messages"])

    return {
        "messages": [response]
    }

# 7. Register nodes
builder.add_node("llm", call_llm)
builder.add_node("tools", tool_node)

# 8. Connect graph
builder.add_edge(START, "llm")
builder.add_conditional_edges(
    "llm",
    tools_condition
)
builder.add_edge("tools", "llm")
# 9. Compile graph
graph = builder.compile()

# 10. Invoke graph
result = graph.invoke({
    "messages": ["Multiply 12 and 10"]
})

print(result["messages"][-1].content)