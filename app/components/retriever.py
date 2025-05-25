# Import required LangChain components for building the QA chain
from langchain.chains import RetrievalQA  # Retrieval-based QA system
from langchain_core.prompts import PromptTemplate  # For custom prompt design

# Import internal functions to load the LLM and vector store
from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

# Import configuration constants like Hugging Face repo ID and token
from app.config.config import HUGGINGFACE_REPO_ID, HF_TOKEN

# Import logger and custom exception handler
from app.common.logger import get_logger  # For consistent logging
from app.common.custom_exception import CustomException  # For structured error reporting

# Import os to check environment variables
import os

# Initialize logger for this module
logger = get_logger(__name__)

# Define a custom prompt template to control the LLM's response format
CUSTOM_PROMPT_TEMPLATE = """Answer the following medical question in 2–3 lines maximum using only the information provided in the context.

Context:
{context}

Question:
{question}

Answer:"""

# Function to initialize a PromptTemplate object with the custom prompt
def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

# Function to create the RetrievalQA chain using vector store and LLM
def create_qa_chain():
    try:
        # Step 1: Load the vector store (FAISS) that contains document embeddings
        logger.info("🔄 Loading vector store...")
        db = load_vector_store()
        
        # If vector store is not found, raise an exception
        if db is None:
            raise CustomException("❌ Vector store is empty. Load PDFs and create embeddings first.")

        # Step 2: Load the language model from Hugging Face
        logger.info("🤖 Initializing LLM for RetrievalQA...")
        logger.info(f"HF_TOKEN Available: {'Yes' if os.getenv('HF_TOKEN') else 'No'}")

        # Load the LLM using specified repo ID and token
        llm = load_llm(huggingface_repo_id=HUGGINGFACE_REPO_ID, hf_token=HF_TOKEN)

        # If LLM is not successfully loaded, raise an exception
        if llm is None:
            raise CustomException("❌ LLM could not be loaded. Check your HF_TOKEN and repo_id.")

        # Step 3: Create the QA chain using the loaded model and vector store
        logger.info("🔗 Creating RetrievalQA chain...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,  # Loaded language model
            chain_type="stuff",  # How to combine the context chunks ("stuff" = simple concatenation)
            retriever=db.as_retriever(search_kwargs={'k': 1}),  # Use retriever to get top 1 relevant chunk
            return_source_documents=False,  # Do not return source docs with the answer
            chain_type_kwargs={'prompt': set_custom_prompt()}  # Use custom prompt template
        )

        # Step 4: Successfully created the QA chain
        logger.info("✅ QA chain successfully created.")
        return qa_chain

    # Catch and log any exceptions that occur during the QA chain setup
    except Exception as e:
        error_message = CustomException("❌ Error while creating QA chain", e)
        logger.error(str(error_message))
        return None  # Return None if something goes wrong
