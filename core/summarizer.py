# core/summarizer.py — fixed: works for any video/audio content, not just meetings

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
    )
    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    llm = get_llm()

    # Step 1 — summarise each chunk independently
    map_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert content analyst. Summarise this portion of a "
            "video or audio transcript concisely. The content may be a meeting, "
            "tutorial, lecture, podcast, or talk — adapt your summary accordingly.",
        ),
        ("human", "{text}"),
    ])
    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)
    chunk_summaries = [map_chain.invoke({"text": chunk}) for chunk in chunks]
    combined = "\n\n".join(chunk_summaries)

    # Step 2 — merge all chunk summaries into one final summary
    reduce_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert content summariser. Combine these partial summaries "
            "into one final, professional summary in clear bullet points.\n"
            "The source may be a meeting, tutorial, lecture, podcast, or talk — "
            "write the summary in the appropriate style.\n"
            "Be concise: 5-8 bullet points maximum.",
        ),
        ("human", "{text}"),
    ])
    reduce_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | reduce_prompt
        | llm
        | StrOutputParser()
    )

    return reduce_chain.invoke(combined)


def generate_title(transcript: str) -> str:
    llm = get_llm()

    title_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            (
                "system",
                "Generate a short, professional title for this video or audio content "
                "(maximum 8 words). The content may be a meeting, tutorial, lecture, "
                "podcast, or talk. Return ONLY the title — no quotes, no extra text.",
            ),
            ("human", "{text}"),
        ])
        | llm
        | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])