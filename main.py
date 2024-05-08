import chainlit as cl
from util.utils import create_retrieval_qa_bot


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

    source_documents = response["source_documents"]

    text_elements = []

    if source_documents:
        for source_doc in source_documents:
            text_elements.append(
                cl.Text(content=source_doc.page_content,
                        name=source_doc.metadata['source'])
            )
        source_names = [txt_el.name for txt_el in text_elements]

        if source_names:
            bot_answer = f"\nSources: {', '.join(source_names)}"
        else:
            bot_answer = "\nNo sources found"

        await cl.Message(content=bot_answer, elements=text_elements).send()
   
