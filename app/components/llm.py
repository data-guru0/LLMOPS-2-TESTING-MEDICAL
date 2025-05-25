# Import the HuggingFaceHub class from LangChain for loading LLMs hosted on Hugging Face
from langchain.llms import HuggingFaceHub

# Import necessary configurations: Hugging Face API token and model repo ID
from app.config.config import HF_TOKEN, HUGGINGFACE_REPO_ID

# Import custom logger and custom exception handler
from app.common.logger import get_logger  # For logging info, warnings, and errors
from app.common.custom_exception import CustomException  # Custom exception class for consistent error formatting

# Initialize logger for the current module
logger = get_logger(__name__)

# Function to load a Hugging Face-hosted LLM using repo ID and token
def load_llm(huggingface_repo_id: str = HUGGINGFACE_REPO_ID, hf_token: str = HF_TOKEN):
    try:
        # Log which model is being loaded
        logger.info(f"✅ Loading LLM from Hugging Face: {huggingface_repo_id}")

        # Instantiate the LLM using HuggingFaceHub with specific model parameters
        llm = HuggingFaceHub(
            repo_id=huggingface_repo_id,  # Model repo ID on Hugging Face
            model_kwargs={
                "temperature": 0.3,           # Controls randomness of output (lower is more deterministic)
                "max_length": 256,            # Max length of generated response
                "return_full_text": False     # Only return the completion, not the full input + completion
            },
            huggingfacehub_api_token=hf_token  # Authorization token to access the model
        )

        # Log successful model loading
        logger.info("🚀 LLM successfully loaded.")

        # Return the LLM instance
        return llm

    # Handle and log any exception that occurs during the model loading process
    except Exception as e:
        error_message = CustomException("❌ Failed to load LLM from Hugging Face", e)

        # Log the error using the custom logger
        logger.error(str(error_message))

        # Return None to gracefully handle failure in the calling function
        return None
