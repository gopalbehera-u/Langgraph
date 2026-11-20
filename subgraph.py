from typing import TypedDict
from langgraph.graph import StateGraph,START,END
class FinanceState(TypedDict):
    income:int
    expense:int
    budget:int
    savings:int
    budget_status:str



def calculate_savings(state:FinanceState):
    income=state['income']
    expense=state['expense']

    saving=income-expense
    return {"savings": saving}


def check_budget(state:FinanceState):
    expense=state['expense']
    budget=state['budget']
    if expense<=budget:
        return {"budget_status": "Within Budget"}
    else:
        return {"budget_status": "Over Budget"}




child_builder=StateGraph(FinanceState)
child_builder.add_node("calculate_savings",calculate_savings)
child_builder.add_node('check_budget',check_budget)

child_builder.add_edge(START,'calculate_savings')
child_builder.add_edge('calculate_savings','check_budget')
child_builder.add_edge('check_budget',END)


child_graph=child_builder.compile()

parent_builder=StateGraph(FinanceState)
parent_builder.add_node("finance_subgraph",child_graph)
parent_builder.add_edge(START,'finance_subgraph')
parent_builder.add_edge('finance_subgraph',END)

parent_graph=parent_builder.compile()



initial_state={
    'income': 50000,
    'expense': 20000,
    'budget': 30000,
    'savings': 0,
    'budget_status': ''
}


result=parent_graph.invoke(initial_state)

print(result)

