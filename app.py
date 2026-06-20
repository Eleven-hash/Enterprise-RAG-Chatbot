import os
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Use absolute paths so it works no matter where the terminal is running from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

st.set_page_config(page_title="RAG Chatbot", page_icon="💬", layout="centered")

def load_vectorstore():
    """Loads the embeddings and the existing Chroma vector database."""
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    # Load the persisted database using absolute path
    db_path = os.path.join(BASE_DIR, "chroma_db")
    vectorstore = Chroma(persist_directory=db_path, embedding_function=embeddings)
    return vectorstore

def setup_rag_chain():
    """Sets up the LLM, prompt templates, and the full conversational RAG chain."""
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # 1. Prompt to reformulate the user's question based on chat history
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

    # 2. Prompt for answering the question based on retrieved context
    qa_system_prompt = """You are a highly knowledgeable and helpful AI assistant.

    CRITICAL INSTRUCTIONS FOR RESPONDING:
    1. GENERAL GREETINGS & SELF-IDENTIFICATION ONLY:
       - If the user's query is a general greeting (e.g., "hi", "hello", "hey"), simple small talk, or a question about your identity/capabilities (e.g., "who are you?", "what is your job?", "how can you help me?"), answer friendly and politely as an AI assistant. You do not need to use the context for these casual conversational queries.
       
    2. ALL OTHER FACTUAL, TECHNICAL, AND TOPIC QUESTIONS:
       - For ALL other queries (including questions about specific documents, tools, deals, or any other factual, general knowledge, or technical questions):
         - You MUST answer the question based strictly and ONLY on the retrieved context below.
         - If the retrieved context does not contain the answer, or does not mention the topic of the question, you MUST politely state that you do not know or that it is not in the provided documents. Do NOT answer using your general knowledge or external information.

    IMPORTANT FORMATTING RULES:
    - Never give a giant wall of text. It overwhelms the user.
    - Break your answer down into very short paragraphs (1-3 sentences maximum).
    - Use bullet points wherever possible to list features, steps, or items.
    - Use **bold text** to highlight key terms or important concepts.
    - Maintain a professional, friendly, and easy-to-digest tone.

    RETIREVED CONTEXT:
    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # 3. Combine them into the final RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("💬 Enterprise RAG Chatbot")
st.markdown("Ask me anything about the **Enterprise RAG** documentation!")

# Load the RAG chain into session state so it doesn't reload or cause caching errors
if "rag_chain" not in st.session_state:
    try:
        with st.spinner("Loading AI Models (this takes a few seconds on startup)..."):
            st.session_state.rag_chain = setup_rag_chain()
    except Exception as e:
        import traceback
        st.error(f"FATAL ERROR:\n\n{traceback.format_exc()}")
        st.stop()

rag_chain = st.session_state.rag_chain

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        st.info(f"**You:** {message['content']}")
    else:
        st.success(f"**AI:** {message['content']}")

# Accept user input
st.markdown("---")
with st.form(key='chat_form', clear_on_submit=True):
    prompt = st.text_input("Ask a question:", placeholder="How do I create a new task?")
    submit_button = st.form_submit_button(label='Send')

if submit_button and prompt:
    # Add user message to chat display
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.info(f"**You:** {prompt}")

    # Generate response
    with st.spinner("Thinking..."):
        try:
            response = rag_chain.invoke({
                "input": prompt,
                "chat_history": st.session_state.chat_history
            })
            answer = response["answer"]
            
            # Render the answer
            st.success(f"**AI:** {answer}")
            
            # Optional: Show sources in an expander
            if "context" in response and response["context"]:
                with st.expander("View Sources"):
                    for i, doc in enumerate(response["context"]):
                        st.write(f"**Source Chunk {i+1}:**")
                        st.text(doc.page_content[:300] + "...")
            
            # Append to display history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Append to LangChain chat history
            st.session_state.chat_history.extend([
                HumanMessage(content=prompt),
                AIMessage(content=answer)
            ])
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
