import os
from pathlib import Path

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from constants import MODEL_KWARGS, MODEL_NAME, QA_CHAIN_PROMPT

ROOT_DIR = Path(__file__).parent.parent.__str__()


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(
        template=QA_CHAIN_PROMPT, input_variables=["context", "question"]
    )
    return prompt


def create_retrieval_qa_chain(llm, prompt, db):
    """
    Empyt docstring
    """
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=2
    )

    retriever = db.as_retriever(search_type="mmr",
                                search_kwargs={"k": 4, "fetch_k": 15})

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={'prompt': prompt},
        return_source_documents=True,
        verbose=True
    )
    return qa_chain


def load_model(
    model="llama2",
    temperature=0.0,
):
    """
    Empyt docstring
    """
    llm = Ollama(model=model, temperature=temperature)

    return llm


def create_retrieval_qa_bot(
    model_name=MODEL_NAME,
    persist_dir=ROOT_DIR + "/db/chroma/",
):
    """
    Empty docstring
    """
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"No directory found at {persist_dir}")

    embedding = HuggingFaceEmbeddings(model_name=model_name,
                                      model_kwargs=MODEL_KWARGS)

    db = Chroma(persist_directory=persist_dir, embedding_function=embedding)

    llm = load_model()

    qa_prompt = (
        set_custom_prompt()
    )

    qa = create_retrieval_qa_chain(
        llm=llm, prompt=qa_prompt, db=db
    )

    return qa


def retrieve_bot_answer(query):
    """
    Empyt docstring
    """
    qa_bot_instance = create_retrieval_qa_bot()
    bot_response = qa_bot_instance({"query": query})
    return bot_response
