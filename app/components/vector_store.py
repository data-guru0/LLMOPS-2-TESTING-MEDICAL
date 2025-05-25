# Import necessary modules
import os  # For checking file system paths

# Import FAISS vector store from LangChain's community module
from langchain_community.vectorstores import FAISS

# Import the function to get the embedding model
from app.components.embeddings import get_embedding_model

# Import path configuration and utilities
from app.config.config import DB_FAISS_PATH  # Path to save/load FAISS DB
from app.common.logger import get_logger  # Logger for tracking info/errors
from app.common.custom_exception import CustomException  # Custom error handler

# Initialize logger for this module
logger = get_logger(__name__)

# Function to load an existing FAISS vector store from disk
def load_vector_store():
    try:
        # Load the embedding model to use for decoding the vectors
        embedding_model = get_embedding_model()

        # Check if the FAISS file exists at the configured path
        if os.path.exists(DB_FAISS_PATH):
            logger.info(f"Loading FAISS vector store from: {DB_FAISS_PATH}")
            return FAISS.load_local(
                DB_FAISS_PATH,
                embedding_model,
                allow_dangerous_deserialization=True  # Enables loading of saved pickle state
            )

        # If FAISS file doesn't exist, return None
        logger.warning("FAISS vector store not found. Returning None.")
        return None

    except Exception as e:
        # Handle and log any errors that occur
        error_message = CustomException("Failed to load FAISS vector store", e)
        logger.error(str(error_message))
        return None

# Function to save a new FAISS vector store to disk using provided text chunks
def save_vector_store(text_chunks):
    try:
        # Ensure that text chunks were passed
        if not text_chunks:
            raise CustomException("No text chunks provided for vector storage.")

        logger.info(f"Generating FAISS vector store with {len(text_chunks)} chunks...")

        # Get the embedding model to generate vector embeddings
        embedding_model = get_embedding_model()

        # Create FAISS vector store from text chunks using the embedding model
        db = FAISS.from_documents(text_chunks, embedding_model)

        logger.info(f"Saving FAISS vector store to: {DB_FAISS_PATH}")

        # Save the FAISS vector store to local disk
        db.save_local(DB_FAISS_PATH)

        logger.info("FAISS vector store saved successfully.")
        return db  # Return the FAISS DB object

    except Exception as e:
        # Handle and log any errors that occur
        error_message = CustomException("Failed to save FAISS vector store", e)
        logger.error(str(error_message))
        return None
