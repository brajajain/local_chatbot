from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl
import os


class ChatModelInitializer:
    @staticmethod
    def initialize_model(model_name):
        """
        Initializes and configures the chat model with a predefined prompt template, indicating the model being used.

        Parameters:
            model_name (str): The name of the model to initialize.

        Returns:
            Runnable: A configured Runnable instance that combines the model, prompt, and output parser.
        """
        # Dynamically update the context to include the model name
        updated_context = f"""
You are a Q&A bot who answers questions by providing comprehensive answers on the evolution of Natural Language Processing (NLP) and Artificial Intelligence (AI), focusing on the development and impact of Generative Pre-trained Transformers (GPTs) and Large Language Models (LLMs). Currently using the {model_name} model.
"""
        model = ChatOllama(model=model_name, streaming=True)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", updated_context),
                ("human", "{question}"),
            ]
        )
        runnable = prompt | model | StrOutputParser()
        return runnable


class SessionManager:
    @staticmethod
    def set_runnable(runnable):
        """
        Stores the runnable instance in the user session.

        Parameters:
            runnable (Runnable): The runnable instance to be stored.
        """
        cl.user_session.set("runnable", runnable)

    @staticmethod
    def get_runnable() -> Runnable:
        """
        Retrieves the runnable instance from the user session.

        Returns:
            Runnable: The runnable instance stored in the user session.
        """
        return cl.user_session.get("runnable")


class MessageHandler:
    @staticmethod
    async def process_message(message: cl.Message, runnable: Runnable):
        """
        Processes an incoming message by running it through the configured runnable instance
        and streaming the output back to the user.

        Parameters:
            message (cl.Message): The incoming message object containing the user's query.
            runnable (Runnable): The runnable instance used to process the query.

        Returns:
            None
        """
        msg = cl.Message(content="")
        async for chunk in runnable.astream(
            {"question": message.content},
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            await msg.stream_token(chunk)
        await msg.send()


@cl.on_chat_start
async def on_chat_start():
    """
    Handles the chat start event by initializing and storing the runnable instance in the user session,
    using the model specified in the command-line arguments.
    """
    model_name = os.getenv("CHAT_MODEL", "llama2")  # Default to 'llama2' if not set
    runnable = ChatModelInitializer.initialize_model(model_name)
    SessionManager.set_runnable(runnable)


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handles incoming messages by retrieving the runnable from the session and processing the message.

    Parameters:
        message (cl.Message): The incoming message from the user.
    """
    runnable = SessionManager.get_runnable()
    await MessageHandler.process_message(message, runnable)
