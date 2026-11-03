from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START,END,StateGraph
from typing import TypedDict
prompt=ChatPromptTemplate.from_template(
    "Explain {topic} in simple  terms "
)
llm=ChatGroq(
    model='qwen/qwen3.8-27b',temperature=0
)
chain=prompt|llm

class ChatState(TypedDict):
    topic:str
    response:str


state:ChatState={
    "topic":"python",'response':''
}

def generate_response(state:ChatState):
    result=chain.invoke({
        "topic":state['topic']
    })
    return {
        'response':result.content
    }

builder=StateGraph(ChatState)
builder.add_node('generateresponse',generate_response)

builder.add_edge(START,'generateresponse')
builder.add_edge('generateresponse',END)


graph=builder.compile()

result=graph.invoke({
      "topic":"langgraph",'response':'' 
})


print(result['response'])


