import argparse
import hashlib
import logging
import shutil
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from app.config import settings
from chroma_db import get

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

logger = logging.getLogger(__name__)


def _load_documents() -> List[Document]:
    loader = PyPDFDirectoryLoader(settings.DOCUMENTS_PATH, glob="*.pdf")
    return loader.load()


def _chunk_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    return splitter.split_documents(documents)


def _encode_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _process_chunks() -> List[Document]:
    documents = _load_documents()
    chunks = _chunk_documents(documents)

    current_source = None
    chunk_index = 0

    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")

        if source != current_source:
            logger.info(f"Processing source: {source}")
            current_source = source
            chunk_index = 0
        else:
            chunk_index += 1

        chunk.metadata.update({
            "id": f"{source}:{page}:{chunk_index}",
            "hash": _encode_text(chunk.page_content)
        })
        logger.info(f"Processed chunk {i} with hash: {chunk.metadata['hash']}, id: {chunk.metadata['id']}")

    return chunks


def update_database(db: Chroma) -> None:
    try:
        existing_docs = db.get()
        existing_docs_by_id = {
            item_id: metadata
            for item_id, metadata in zip(existing_docs["ids"], existing_docs["metadatas"])
        }

        logger.info(f"Found {len(existing_docs['ids'])} existing documents in DB ✅")
        chunks = _process_chunks()

        new_chunks = []
        for chunk in chunks:
            chunk_id = chunk.metadata["id"]
            chunk_hash = chunk.metadata["hash"]

            if chunk_id not in existing_docs_by_id:
                new_chunks.append(chunk)
            elif existing_docs_by_id[chunk_id]["hash"] != chunk_hash:
                logger.info(f"Updating changed chunk: {chunk_id}")
                db.update_document(chunk_id, chunk)

        if new_chunks:
            logger.info(f"Adding {len(new_chunks)} new documents ✅")
            db.add_documents(
                new_chunks,
                ids=[chunk.metadata["id"] for chunk in new_chunks]
            )
        else:
            logger.info("No new documents to add")

    except Exception as e:
        logger.error(f"Error updating database: {str(e)}")
        raise


def clear_database() -> None:
    try:
        if Path(settings.CHROMA_PATH).exists():
            shutil.rmtree(settings.CHROMA_PATH)
            logger.info("Database cleared successfully ✅")
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)} ❌")
        raise


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--clear", action="store_true", help="Clear the database before updating")

        args = parser.parse_args()
        if args.clear:
            logger.info("Clearing database...")
            clear_database()

        db = get()
        update_database(db)
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)} ❌")
        raise


if __name__ == '__main__':
    main()

