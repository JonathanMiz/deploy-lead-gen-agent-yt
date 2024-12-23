import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AIRTABLE_API_KEY: str
    AIRTABLE_BASE_ID: str
    RESOURCES_PATH: str = "resources"
    DOCUMENTS_PATH = os.path.join(RESOURCES_PATH, "docs")
    CHROMA_PATH = os.path.join(RESOURCES_PATH, "chroma")


settings = Settings()