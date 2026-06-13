# core/rage.py — fixed: works for any video/audio content, not just meetings

import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.vectorStore import build_vector_store, load_vector_store, get_retriever


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )


def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


def build_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)
    retriever = get_retriever(vector_store, k=4)
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an intelligent assistant that has fully analysed a video or audio transcript.
Answer the user's question based ONLY on the transcript context provided below.

Guidelines:
- Be concise, clear, and precise.
- If the transcript is a tutorial or lecture, answer as an expert on that topic.
- If the transcript is a meeting, answer as a meeting analyst.
- If the answer is not in the context, say: "I could not find this information in the transcript."
- If quoting the speaker directly, make it clear with quotation marks.

Transcript context:
{context}""",
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store)
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an intelligent assistant that has fully analysed a video or audio transcript.
Answer the user's question based ONLY on the transcript context provided below.

Guidelines:
- Be concise, clear, and precise.
- If the transcript is a tutorial or lecture, answer as an expert on that topic.
- If the transcript is a meeting, answer as a meeting analyst.
- If the answer is not in the context, say: "I could not find this information in the transcript."
- If quoting the speaker directly, make it clear with quotation marks.

Transcript context:
{context}""",
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question: str) -> str:
    print(f"Question: {question}")
    answer = rag_chain.invoke(question)
    print(f"Answer: {answer}")
    return answer