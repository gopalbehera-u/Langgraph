from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import uuid
from langgraph.graph import START,END,StateGraph,MessagesState

llm=ChatGroq(
    model='qwen/qwen3.8-27b',temperature=0
)

memory=InMemorySaver()
def call_llm(state:MessagesState):
    response=llm.invoke(state['messages'])
    return {'messages':[response]}
builder = StateGraph(MessagesState)

builder.add_node("llm", call_llm)

builder.add_edge(START, "llm")
builder.add_edge("llm", END)


graph=builder.compile(checkpointer=memory)

# thread_id=str(uuid.uuid4())
def threadconfig():
    thread_id = str(uuid.uuid4())

    return {
        "configurable": {
            "thread_id": thread_id
        }
    }



config=threadconfig()
print(config)
config2=threadconfig()
print(config2)



result1=graph.invoke(
    {"messages": ["My favourite programming language is Python."]},
    config=config
)

snapshot=graph.get_state(config)

# print(snapshot.values['messages'])
print(snapshot.next)
print(snapshot.metadata)

print(snapshot.config)
# print(result1['messages'][-1].content)

# result2 = graph.invoke({
#     "messages": ["What is my favourite programming language?"]


#     },    config=config
# )
# result3 = graph.invoke({
#     "messages": ["i want to become an ai engineer?"]


#     },    config=config
# )



# print(result3['messages'][-1].content)



# result4 = graph.invoke({
#     "messages": ["now tell me i want to become and my fav programing language "]


#     },    config=config
# )



# print(result4['messages'][-1].content)


# result11=graph.invoke(
#     {"messages": ["what is my fav programing language ."]},
#     config=config2
# )

# print(result11['messages'][-1].content)

