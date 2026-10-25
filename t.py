import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
llm = init_chat_model(os.getenv("LLM_MODEL"), model_provider="google_genai", temperature=0)
res=llm.invoke("OK")
print(res.text)