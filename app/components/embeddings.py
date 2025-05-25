# Import the HuggingFaceEmbeddings class to create embedding models
from langchain_huggingface import HuggingFaceEmbeddings

# Import custom logger and exception handler
from app.common.logger import get_logger  # For consistent logging across the app
from app.common.custom_exception import CustomException  # Custom exception for better error handling

# Initialize logger for this module
logger = get_logger(__name__)

# Function to initialize and return a Hugging Face embedding model
def get_embedding_model():
    try:
        # Log the start of model initialization
        logger.info("🔍 Initializing Hugging Face Embedding Model...")

        # Load the sentence-transformer model for generating text embeddings
        model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Log successful model loading
        logger.info("✅ Hugging Face Embedding Model successfully loaded.")

        # Return the loaded model instance
        return model

    # Catch and log any errors during the model loading process
    except Exception as e:
        error_message = CustomException("Error occurred while loading the embedding model.", e)

        # Log the custom error message
        logger.error(str(error_message))

        # Raise the custom exception so it can be handled upstream if needed
        raise error_message
