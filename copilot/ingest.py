import shutil
import time

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from copilot import config

def load_pages(pdf_path):
    docs=[]
    for n,page in enumerate(PdfReader(pdf_path).pages,start=1):
        if n in config.SKIP_PAGES:
            continue
        text=(page.extract_text()or"").strip()
        if len(text)<50:
            continue
        docs.append(Document(page_content=text,metadata={"source":pdf_path.name,"page":n}))
    return docs

def add_with_retry(store,batch,essais=5):
    for essai in range(1,essais+1):
        try:
            store.add_documents(batch)
            return
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                att=45*essai
                print(f"quota atteint, nouvelle tentative dans {att}s ({essai}/{essais})")
                time.sleep(att)
            else:
                raise
    raise RuntimeError("Quota dépassé !!!")


def main():
    docs = []
    for pdf in sorted(config.MANUALS_DIR.glob("*.pdf")):
        docs+=load_pages(pdf)
    print(f"{len(docs)} pages retenues")

    sp=RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE,chunk_overlap=config.CHUNK_OVERLAP)
    chunks=sp.split_documents(docs)   # les métadonnées sont conservées
    print(f"{len(chunks)} passages")

    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)      
    embeddings=GoogleGenerativeAIEmbeddings(model=config.EMBED_MODEL)
    store=Chroma(embedding_function=embeddings,persist_directory=str(config.CHROMA_DIR))

    for i in range(0,len(chunks),config.BATCH):
        add_with_retry(store,chunks[i:i+config.BATCH])
        print(f"-- {min(i+config.BATCH,len(chunks))}/{len(chunks)}")
        time.sleep(config.PAUSE)


if __name__ == "__main__":
    main()