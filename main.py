import os

import chainlit as cl
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from constants import MODEL_KWARGS, MODEL_NAME, QA_CHAIN_PROMPT


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
                                search_kwargs={"k": 2, "fetch_k": 3})
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
    persist_dir="db/chroma/",
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


@cl.on_chat_start
async def initialize_bot():
    """
    Initializes the bot when a new chat starts.

    This asynchronous function creates a new instance of the retrieval QA bot,
    sends a welcome message, and stores the bot instance in the user's session.
    """
    qa_chain = create_retrieval_qa_bot()
    welcome_message = cl.Message(content="Starting the bot...")
    await welcome_message.send()
    welcome_message.content = (
        "Hi, Welcome to Chat With Documents using Llama2 and LangChain."
    )
    await welcome_message.update()

    cl.user_session.set("chain", qa_chain)


@cl.on_message
async def process_chat_message(message):
    """
    Processes incoming chat messages.

    This asynchronous function retrieves the QA bot instance from the user's
    session, sets up a callback handler for the bot's response,
    and executes the bot's call method with the given message and callback.
    The bot's answer and source documents are then extracted from the response.
    """

    qa_chain = cl.user_session.get("chain")
    callback_handler = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    callback_handler.answer_reached = True
    response = await qa_chain.acall(message.content,
                                    callbacks=[callback_handler])
    bot_answer = response["answer"]
    source_documents = response["source_documents"]

    text_elements = []

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [txt_el.name for txt_el in text_elements]

        if source_names:
            bot_answer += f"\nSources: {', '.join(source_names)}"
        else:
            bot_answer += "\nNo sources found"

    await cl.Message(content=bot_answer, elements=text_elements).send()
