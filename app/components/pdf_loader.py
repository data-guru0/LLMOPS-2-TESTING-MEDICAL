import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_pdf_files():
    try:
        if not os.path.exists(DATA_PATH):
            raise CustomException(f"Data path '{DATA_PATH}' does not exist.")

        logger.info(f"Loading PDF files from: {DATA_PATH}")
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()

        if not documents:
            logger.warning("No PDF documents found in the directory.")
        else:
            logger.info(f"Successfully loaded {len(documents)} documents.")

        return documents

    except Exception as e:
        error_message = CustomException("Failed to load PDF files", e)
        logger.error(str(error_message))
        return []

def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No documents provided for text splitting.")

        logger.info(f"Splitting {len(documents)} documents into chunks...")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        text_chunks = text_splitter.split_documents(documents)

        logger.info(f"Generated {len(text_chunks)} text chunks.")
        return text_chunks

    except Exception as e:
        error_message = CustomException("Failed to create text chunks", e)
        logger.error(str(error_message))
        return []