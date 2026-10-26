from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from copilot import config


def get_store():
    emb=GoogleGenerativeAIEmbeddings(model=config.EMBED_MODEL)
    return Chroma(embedding_function=emb,persist_directory=str(config.CHROMA_DIR))


if __name__ == "__main__":
    q=input("Question : ")
    for doc in get_store().similarity_search(q,k=config.TOP_K):
        print(f"\n--- p:{doc.metadata['page']} ---")
        print(doc.page_content[:300])