from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import START,END,StateGraph,MessagesState
from langchain.tools import tool
llm=ChatGroq(
    model='qwen/qwen3.8-27b',temperature=0
)

def call_llm(state:MessagesState):
    response=llm.invoke(state['messages'])
    return {'messages':[response]}


builder=StateGraph(MessagesState)
builder.add_node('llm',call_llm)
builder.add_edge(START,'llm')
builder.add_edge('llm',END)
graph=builder.compile()

# result1 = graph.invoke({
#     "messages": ["My name is Gopal."]
# })

result2 = graph.invoke({
    "messages": ["My name is Gopal","What is my name?"]
})

# print(result1['messages'][-1].content)
print(result2['messages'][-1].content)
