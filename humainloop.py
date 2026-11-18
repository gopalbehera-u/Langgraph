from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt,Command
from  langgraph.checkpoint.memory import InMemorySaver

class ExpenseState(TypedDict):
    expense:int
    reason:str
    status:str

checkpointer = InMemorySaver()

def approval_node(state: ExpenseState):
    decision = interrupt("Do you want to approve this expense?")

    if decision == "approve":
        return {"status": "approved"}
    else:
        return {"status": "rejected"}




builder=StateGraph(ExpenseState)
builder.add_node("approval",approval_node)
builder.add_edge(START,'approval')
builder.add_edge('approval',END)


graph=builder.compile(checkpointer=checkpointer)

config1={
    "configurable":{
        "thread_id":"expense_001"
    }
}

config2={
    "configurable":{
        "thread_id":"expense_002"
    }
}


result1=graph.invoke({
    "expense":10000,"reason":"buy a laptop",'status':'pending'
},config=config1)


result2=graph.invoke(
    Command(resume='approve'),config=config1
)

result3=graph.invoke({
    'expense':10000,'reason':'buy a laptop','status':'pending'
},config=config2)

result4=graph.invoke(
    Command(resume='rejected'),config=config2
)


# print(result2['status'])
# print(result4['status'])


config={
    "configurable":{
            "thread_id":"expense_day16"
        }
}

result=graph.invoke({
    "expense":10000,'reason':"Buy a laptop",'status':'pending'
},config=config)


graph.update_state(
    config,{'expense':8000}
)

snapshot=graph.get_state(config)


# print(snapshot.values['expense'])

# print(snapshot.next)
# print(snapshot.tasks)


# result2 = graph.invoke(None, config=config)

# print(result2)


result3=graph.invoke(
    Command(resume='approve'),config
)

print(result3['expense'])
print(result3['status'])
