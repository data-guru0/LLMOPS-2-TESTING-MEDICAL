# Import necessary modules
import os
from app.components.pdf_loader import load_pdf_files, create_text_chunks  # Functions to load and chunk PDF data
from app.components.vector_store import save_vector_store  # Function to save vector embeddings to FAISS
from app.config.config import DB_FAISS_PATH  # Configuration path for the FAISS vector store
from app.common.logger import get_logger  # Custom logger for logging
from app.common.custom_exception import CustomException  # Custom exception class for structured error handling

# Initialize the logger for this module
logger = get_logger(__name__)

# Function to process PDFs and store their vector embeddings
def process_and_store_pdfs():
    try:
        # Log the start of the PDF processing pipeline
        logger.info("🔄 Starting PDF processing...")

        # Load all PDF files from the expected directory
        documents = load_pdf_files()

        # If no documents were found, log a warning and exit
        if not documents:
            logger.warning("⚠️ No PDF files found in the data/ directory.")
            return
        
        # Log the number of PDF pages successfully loaded
        logger.info(f"📄 Successfully loaded {len(documents)} PDF pages.")

        # Convert loaded documents into smaller text chunks
        text_chunks = create_text_chunks(documents)

        # Log the number of text chunks created
        logger.info(f"🔹 Created {len(text_chunks)} text chunks.")

        # Log the start of the vector store creation
        logger.info("🔍 Generating vector embeddings and saving to FAISS...")

        # Save the text chunks as vector embeddings into the FAISS vector store
        save_vector_store(text_chunks)

        # Log the successful saving of the vector store
        logger.info(f"✅ FAISS vector store successfully saved at: {DB_FAISS_PATH}")

    # Catch any exception during the process and log it using the custom exception
    except Exception as e:
        error_message = CustomException("Error occurred during PDF processing and vector storage.", e)
        logger.error(str(error_message))

# Execute the function if the script is run as the main module
if __name__ == "__main__":
    process_and_store_pdfs()
