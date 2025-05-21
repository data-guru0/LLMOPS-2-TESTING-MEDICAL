import os
from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.components.vector_store import save_vector_store
from app.config.config import DB_FAISS_PATH
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_pdfs():
    try:
        logger.info("🔄 Starting PDF processing...")


        documents = load_pdf_files()
        if not documents:
            logger.warning("⚠️ No PDF files found in the data/ directory.")
            return
        
        logger.info(f"📄 Successfully loaded {len(documents)} PDF pages.")


        text_chunks = create_text_chunks(documents)
        logger.info(f"🔹 Created {len(text_chunks)} text chunks.")

        logger.info("🔍 Generating vector embeddings and saving to FAISS...")
        save_vector_store(text_chunks)
        logger.info(f"✅ FAISS vector store successfully saved at: {DB_FAISS_PATH}")

    except Exception as e:
        error_message = CustomException("Error occurred during PDF processing and vector storage.", e)
        logger.error(str(error_message))

if __name__ == "__main__":
    process_and_store_pdfs()