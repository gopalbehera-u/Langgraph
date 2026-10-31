from typing import TypedDict

def calculate_expenses(state):
    total=800.0
    return {"total":total}




def ans_expene(state):
    total=state['total']
    ans=f" you spent {total} on food"
    return {"answer":ans}