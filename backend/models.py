from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

openai = init_chat_model("openai:gpt-4.1-mini")
# ollama = init_chat_model("ollama:llama3.2")
