from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl

context = """You are a Q&A bot who answers questions by providing comprehensive answers on the evolution of Natural Language Processing (NLP) and Artificial Intelligence (AI), focusing on the development and impact of Generative Pre-trained Transformers (GPTs) and Large Language Models (LLMs)."""


@cl.on_chat_start
async def on_chat_start():
    model = ChatOllama(model="llama2", streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", context),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
