# Import necessary modules for building the Flask web app
from flask import Flask, render_template, request, session, redirect, url_for
from app.components.retriever import create_qa_chain  # Function to create QA chain
from dotenv import load_dotenv  # To load environment variables from .env
import os  # For accessing environment variables and file system

# Load environment variables from .env file
load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")  # Get Hugging Face token from env variables

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session handling

# Import Markup from Jinja for safe HTML rendering
from markupsafe import Markup

# Define a Jinja2 filter to convert newline characters to <br> for HTML rendering
def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

# Register the filter with the Jinja environment
app.jinja_env.filters['nl2br'] = nl2br

# Route for home page with GET and POST methods
@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize session messages if not already present
    if "messages" not in session:
        session["messages"] = []

    # Handle POST request (i.e., user submitted a prompt)
    if request.method == "POST":
        user_input = request.form.get("prompt")  # Get user input from form

        if user_input:
            # Append user message to session chat history
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})
            session["messages"] = messages  # Update session

            try:
                # Create the QA chain for LLM interaction
                qa_chain = create_qa_chain()

                # Query the chain with user's input and get result
                response = qa_chain.invoke({"query": user_input})
                result = response.get("result", "No response")

                # Append assistant response to session chat history
                messages.append({"role": "assistant", "content": result})
                session["messages"] = messages  # Update session

            except Exception as e:
                # If there's an error, show the error message on the page
                error_msg = f"Error: {str(e)}"
                return render_template("index.html", messages=session["messages"], error=error_msg)

        # After processing POST request, redirect to index to prevent form resubmission
        return redirect(url_for("index"))

    # Handle GET request: render chat UI with previous messages (if any)
    return render_template("index.html", messages=session.get("messages", []))

# Route to clear the chat history from the session
@app.route("/clear")
def clear():
    session.pop("messages", None)  # Remove messages from session
    return redirect(url_for("index"))  # Redirect to home page

# Run the Flask app only if this file is executed directly
if __name__ == "__main__":
    # Bind to all IPs (0.0.0.0) on port 5000, with debug and reloader disabled
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
