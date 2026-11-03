from langgraph.graph import StateGraph,START,END,MessagesState
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import tools_condition,ToolNode
from langgraph.runtime import Runtime
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)
@tool
def multiply(a:float,b:float):
    """Multiply two numbers, a and b."""
    return a*b
@tool
def add(a:float,b:float):
    """Add two numbers, a and b."""
    return a+b

ll_with_tool=llm.bind_tools([multiply,add])
tool_node=ToolNode([multiply,add])


# respsonse=ll_with_tool.invoke('What is the addition of 5 and 33?')

# result = tool_node.invoke(
#     {"messages": [respsonse]},
#     runtime=Runtime()
# )

def call_llm(state:MessagesState):
    response=ll_with_tool.invoke(state["messages"])
    return {'message':[response]}
def call_llm(state: MessagesState):
    response = ll_with_tool.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("callllm", call_llm)
builder.add_node("tools", tool_node)

builder.add_edge(START, "callllm")

builder.add_conditional_edges(
    "callllm",
    tools_condition
)

builder.add_edge("tools", "callllm")

graph = builder.compile()

result = graph.invoke({
    "messages": ["Multiply 12 and 10  and addition of 5 and 45 "]
})

print(result["messages"][-1].content)