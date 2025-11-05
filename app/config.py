import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set model configuration
MODEL_NAME = "gemini-2.5-flash"  # Use 1.5-flash or 1.5-pro for better non-tool use
