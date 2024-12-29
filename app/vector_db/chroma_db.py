import sys, os, pathlib
sys.path.append(os.path.join(pathlib.Path(__file__).parent.parent.parent))

from app.config import settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


_db_instance = None


def get():
    global _db_instance
    if _db_instance is None:
        embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        _db_instance = Chroma(
            persist_directory=str(settings.CHROMA_PATH),
            embedding_function=embeddings
        )
    return _db_instance
