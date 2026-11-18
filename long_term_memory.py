from langgraph.store.memory import InMemoryStore
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import uuid
from langgraph.graph import START,END,StateGraph,MessagesState

store=InMemoryStore()

namespace=("user_123","preferences")
key="favourite_language"

value={'language':'Python'}


store.put(namespace,key,value)
item= store.get(namespace,key)
print(item.value)


result=store.search(namespace)

for item in result:
    print(item.key,item.value)
