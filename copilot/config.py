import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT=Path(__file__).resolve().parent.parent
MANUALS_DIR=ROOT/"data"/"manuals"
CHROMA_DIR=ROOT/"chroma_db"
LLM_MODEL=os.getenv("LLM_MODEL","gemini-3.5-flash")
EMBED_MODEL=os.getenv("EMBED_MODEL","gemini-embedding-001")  
CHUNK_SIZE=int(os.getenv("CHUNK_SIZE","1000"))
CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP","150"))
TOP_K=int(os.getenv("TOP_K","4"))
SKIP_PAGES={int(p) for p in os.getenv("SKIP_PAGES", "").split(",") if p.strip()}
BATCH=40         
PAUSE=30 # éviter de dépasser les limites de requêtes ou de consommation Google
