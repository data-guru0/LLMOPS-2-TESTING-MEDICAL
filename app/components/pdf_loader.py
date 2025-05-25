# Import necessary modules
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader  # Loaders to read PDF files from a directory
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into manageable chunks

# Import project-specific configuration constants
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP  # Paths and chunking settings

# Import custom logger and exception handling
from app.common.logger import get_logger  # For logging informational and error messages
from app.common.custom_exception import CustomException  # Custom wrapper for exceptions

# Initialize logger for this module
logger = get_logger(__name__)

# Function to load all PDF files from a specified directory
def load_pdf_files():
    try:
        # Check if the data path exists
        if not os.path.exists(DATA_PATH):
            raise CustomException(f"Data path '{DATA_PATH}' does not exist.")  # Raise custom exception if path is invalid

        # Log the path from where PDFs are being loaded
        logger.info(f"Loading PDF files from: {DATA_PATH}")

        # Use DirectoryLoader with PyPDFLoader to read all .pdf files in the directory
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)

        # Load the PDF documents
        documents = loader.load()

        # Log how many documents were loaded or warn if none were found
        if not documents:
            logger.warning("No PDF documents found in the directory.")
        else:
            logger.info(f"Successfully loaded {len(documents)} documents.")

        # Return the loaded documents (even if it's an empty list)
        return documents

    # Handle and log any exceptions that occur during loading
    except Exception as e:
        error_message = CustomException("Failed to load PDF files", e)
        logger.error(str(error_message))
        return []  # Return an empty list on failure

# Function to split loaded documents into smaller text chunks
def create_text_chunks(documents):
    try:
        # Raise an exception if the input document list is empty
        if not documents:
            raise CustomException("No documents provided for text splitting.")

        # Log how many documents will be split
        logger.info(f"Splitting {len(documents)} documents into chunks...")

        # Initialize the text splitter with the configured chunk size and overlap
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

        # Split the documents into chunks
        text_chunks = text_splitter.split_documents(documents)

        # Log how many chunks were created
        logger.info(f"Generated {len(text_chunks)} text chunks.")

        # Return the generated chunks
        return text_chunks

    # Handle and log any exceptions that occur during chunk creation
    except Exception as e:
        error_message = CustomException("Failed to create text chunks", e)
        logger.error(str(error_message))
        return []  # Return an empty list on failure
