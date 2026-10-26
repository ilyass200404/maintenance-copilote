import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
client=genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
noms=[m.name for m in client.models.list() if "embed" in m.name]
print("-- Embeddings :",noms)

emb=GoogleGenerativeAIEmbeddings(model=noms[0])
v=emb.embed_query("!!!")
print(noms[0],"a pour dimension :",len(v))