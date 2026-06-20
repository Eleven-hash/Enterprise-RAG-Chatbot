import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    return vectorstore

def setup_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = """You are a highly knowledgeable and helpful AI assistant.

    CRITICAL INSTRUCTIONS FOR RESPONDING:
    1. GENERAL GREETINGS & SELF-IDENTIFICATION ONLY:
       - If the user's query is a general greeting, simple small talk, or a question about your identity/capabilities, answer friendly and politely as an AI assistant. You do not need to use the context for these casual conversational queries.
       
    2. ALL OTHER FACTUAL, TECHNICAL, AND TOPIC QUESTIONS:
       - For ALL other queries (including questions about specific documents, tools, deals, or any other factual, general knowledge, or technical questions):
         - You MUST answer the question based strictly and ONLY on the retrieved context below.
         - If the retrieved context does not contain the answer, or does not mention the topic of the question, you MUST politely state that you do not know.

    RETIREVED CONTEXT:
    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

if __name__ == "__main__":
    try:
        setup_rag_chain()
        print("RAG CHAIN SETUP SUCCESSFUL!")
    except Exception as e:
        import traceback
        traceback.print_exc()
