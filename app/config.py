import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('chromadb').setLevel(logging.WARNING)

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AIRTABLE_API_KEY: str
    AIRTABLE_BASE_ID: str
    RESOURCES_PATH: str = "resources"
    DOCUMENTS_PATH: str = os.path.join(RESOURCES_PATH, "docs")
    CHROMA_PATH: str = os.path.join(RESOURCES_PATH, "chroma")


settings = Settings()