from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import START,END,StateGraph,MessagesState
from langgraph.runtime import Runtime
from langgraph.prebuilt import ToolNode,tools_condition
from langchain.tools import tool
llm=ChatGroq(
    model='qwen/qwen3.8-27b',temperature=0
)

@tool
def add(a:float,b:float):
    "add two numbers"
    return a+b
@tool
def multiply(a:float,b:float):
    "multiply two number "
    return a*b 
@tool
def divide(a:float,b:float):
    "divide two number"
    return a/b
@tool
def subtract(a: float, b: float):
    "substarct these numbers "
    return a - b
llm_with_tool=llm.bind_tools([add,multiply,divide])
toolnode=ToolNode([add,multiply,divide],handle_tool_errors=True)

def call_llm(state:MessagesState):
    response=llm_with_tool.invoke(state['messages'])
    return {'messages':[response]}

builder=StateGraph(MessagesState)
builder.add_node('llm',call_llm)
builder.add_node('tools',toolnode)

builder.add_edge(START,'llm')
builder.add_conditional_edges('llm',tools_condition)
builder.add_edge('tools','llm')
builder.add_edge('llm',END)

graph=builder.compile()

result=graph.invoke({
    "messages": ["Substarction  10 and  20"]
})

print(result['messages'][-1].content)