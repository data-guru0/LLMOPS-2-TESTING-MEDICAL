import os
from langchain_community.vectorstores import FAISS
from app.components.embeddings import get_embedding_model
from app.config.config import DB_FAISS_PATH
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_vector_store():
    try:
        embedding_model = get_embedding_model()

        if os.path.exists(DB_FAISS_PATH):
            logger.info(f"Loading FAISS vector store from: {DB_FAISS_PATH}")
            return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

        logger.warning("FAISS vector store not found. Returning None.")
        return None

    except Exception as e:
        error_message = CustomException("Failed to load FAISS vector store", e)
        logger.error(str(error_message))
        return None

def save_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise CustomException("No text chunks provided for vector storage.")

        logger.info(f"Generating FAISS vector store with {len(text_chunks)} chunks...")

        embedding_model = get_embedding_model()
        db = FAISS.from_documents(text_chunks, embedding_model)

        logger.info(f"Saving FAISS vector store to: {DB_FAISS_PATH}")
        db.save_local(DB_FAISS_PATH)

        logger.info("FAISS vector store saved successfully.")
        return db

    except Exception as e:
        error_message = CustomException("Failed to save FAISS vector store", e)
        logger.error(str(error_message))
        return None