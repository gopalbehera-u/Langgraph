from langchain_moonshot import ChatMoonshot
from dotenv import load_dotenv
load_dotenv()
llm=ChatMoonshot(
    model="kimi-k2.5",
    temperature=1.0
)


result=llm.invoke("what is an llm")
print(result.content)