import os

# 1. Directory Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")
DATA_DIRECTORY = os.path.join(BASE_DIR, "data")

# 2. Text Chunking Configurations
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNK_SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n", " ", ""]

# 3. Model Configurations
EMBEDDING_MODEL = "BAAI/bge-m3"
LLM_MODEL = "gpt-4o-mini"

# 4. Retrieval Configurations
RETRIEVAL_K = 3

# 5. Guardrail Configurations
MAX_QUERY_LENGTH = 800
