import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import config

load_dotenv()
def main():
    # 1. Load the documents from the data directory recursively
    data_dir = config.DATA_DIRECTORY
    print(f"Loading documents recursively from directory: {data_dir}")
    if not os.path.exists(data_dir):
        print(f"Error: Directory '{data_dir}' not found.")
        return

    # DirectoryLoader will find all markdown files recursively in the folder
    loader = DirectoryLoader(data_dir, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    all_documents = loader.load()
    print(f"Loaded {len(all_documents)} document(s) in total.")
    
    if len(all_documents) == 0:
        print("No documents found in the data folder.")
        return

    # 2. Split the document into chunks
    print("Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=config.CHUNK_SEPARATORS
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"Created {len(chunks)} chunks.")

    # 3. Initialize Embeddings
    print(f"Initializing HuggingFace Embeddings ({config.EMBEDDING_MODEL})...")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # 4. Create and persist Vector Store (ChromaDB)
    persist_directory = config.PERSIST_DIRECTORY
    print(f"Creating ChromaDB vector store at: {persist_directory}")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("Vector store created successfully.")

    # 5. Setup LLM and Generation Chain
    print(f"Initializing LLM (OpenAI {config.LLM_MODEL})...")
    # Make sure your OPENAI_API_KEY is set in your environment variables or a .env file!
    llm = ChatOpenAI(model_name=config.LLM_MODEL, temperature=0)

    prompt = ChatPromptTemplate.from_template("""You are a highly knowledgeable and helpful AI assistant.

CRITICAL INSTRUCTIONS FOR RESPONDING:
1. GENERAL GREETINGS & SELF-IDENTIFICATION ONLY:
   - If the user's query is a general greeting, simple small talk, or a question about your identity/capabilities, answer friendly and politely as an AI assistant. You do not need to use the context for these casual conversational queries.
   
2. ALL OTHER FACTUAL, TECHNICAL, AND TOPIC QUESTIONS:
   - For ALL other queries (including questions about specific documents, tools, deals, or any other factual, general knowledge, or technical questions):
     - You MUST answer the question based strictly and ONLY on the retrieved context below.
     - If the retrieved context does not contain the answer, or does not mention the topic of the question, you MUST politely state that you do not know.

RETIREVED CONTEXT:
{context}

Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever(search_kwargs={"k": config.RETRIEVAL_K})
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # 6. Test Retrieval and Generation
    query = "What fields are required to create a task?"
    print(f"\n--- Testing RAG ---")
    print(f"Query: '{query}'")
    
    response = retrieval_chain.invoke({"input": query})
    
    print(f"\nAnswer:")
    print(response["answer"])
    
    print("\n--- Source Documents Used ---")
    for i, doc in enumerate(response["context"]):
        print(f"Chunk {i+1}:\n{doc.page_content[:150]}...\n")
        
    print("-" * 50)

if __name__ == "__main__":
    main()
