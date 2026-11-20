from typing import TypedDict,Annotated
from langgraph.graph import StateGraph,START,END
import operator
class FinanceState(TypedDict):
    income:int
    expense:int
    budget:int
    results:Annotated[list[str],operator.add]


def finance_data(state:FinanceState):
    income=state['income']
    expense=state['expense']
    budget=state['budget']

    print("Income : ",income)
    print("Expense : ",expense)
    print("Budget : ",budget)

    return {}


def expense_analysis(state:FinanceState):
    income=state['income']
    expense=state['expense']

    expensepercntage=(expense/income)*100

    return {"results":[f"Expense percentage : {expensepercntage}%"]}



def saving_calculation(state:FinanceState):
    income=state['income']
    expense=state['expense']
    saving=income-expense
    return  {"results": [f"Total savings: ₹{saving}"]}


def budget_check(state:FinanceState):
    expense=state['expense']
    budget=state['budget']
    if expense <= budget:
        return {"results": [f"Within budget. Remaining: ₹{budget-expense}"]}
    else:
        return {"results": [f"Over budget by ₹{expense-budget}"]}




def final_report(state:FinanceState):
    results=state['results']
    print("FINAL FINANCIAL REPORT")
    for result in results:
        print(result)
    return {}

builder=StateGraph(FinanceState)
builder.add_node("finance_data",finance_data)
builder.add_node("expense_analysis",expense_analysis)
builder.add_node("saving_calculation",saving_calculation)
builder.add_node('budget_check',budget_check)
builder.add_node("final_report",final_report)

builder.add_edge(START,'finance_data')
builder.add_edge('finance_data','expense_analysis')
builder.add_edge('finance_data','saving_calculation')
builder.add_edge('finance_data','budget_check')

builder.add_edge(
    ["expense_analysis", "saving_calculation", "budget_check"],
    "final_report"
)

builder.add_edge("final_report", END)



graph=builder.compile()

initial_state={
    'income':50000,
    'expense':20000,
    'budget':30000,
    'results':[]
}

result=graph.invoke(initial_state)
print(result)