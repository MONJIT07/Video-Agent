# core/extractor.py — fixed: works for ANY video/audio content, not just meetings

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os
import re


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2,
    )


def build_chain(system_prompt: str):
    llm = get_llm()
    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}"),
        ])
        | llm
        | StrOutputParser()
    )


def _truncate(transcript: str, max_chars: int = 12_000) -> str:
    """Keep transcript within Mistral context limits."""
    if len(transcript) <= max_chars:
        return transcript
    half = max_chars // 2
    return transcript[:half] + "\n\n[...middle section omitted...]\n\n" + transcript[-half:]


def extract_action_items(transcript: str) -> str:
    chain = build_chain(
        "You are an expert content analyst. The text below may be a meeting, "
        "a YouTube tutorial, a lecture, a podcast, or any spoken content.\n\n"
        "Your task: extract EVERY concrete action, task, recommendation, or "
        "step that a person should DO based on this content.\n\n"
        "Rules:\n"
        "- Output ONLY a clean numbered list (1. 2. 3. ...), nothing else.\n"
        "- Each item must be one clear, actionable sentence.\n"
        "- For tutorials/lectures: list the steps, techniques, or practices taught.\n"
        "- For meetings: list tasks assigned and who should do them.\n"
        "- ALWAYS produce at least 3 items — never say 'No action items found'.\n"
        "- If content is vague, list logical follow-up actions a viewer should take.\n"
        "- Do NOT add intros, headers, markdown, or any text outside the list."
    )
    return chain.invoke(_truncate(transcript))


def extract_key_decisions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert content analyst. The text below may be a meeting, "
        "a YouTube tutorial, a lecture, a podcast, or any spoken content.\n\n"
        "Your task: extract the KEY POINTS, decisions, conclusions, or "
        "main takeaways from this content.\n\n"
        "Rules:\n"
        "- Output ONLY a clean numbered list (1. 2. 3. ...), nothing else.\n"
        "- For meetings: list actual decisions made.\n"
        "- For tutorials/lectures: list the core concepts or conclusions presented.\n"
        "- ALWAYS produce at least 3 items — never say 'No key decisions found'.\n"
        "- Do NOT add intros, headers, markdown, or any text outside the list."
    )
    return chain.invoke(_truncate(transcript))


def extract_questions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert content analyst. The text below may be a meeting, "
        "a YouTube tutorial, a lecture, a podcast, or any spoken content.\n\n"
        "Your task: extract OPEN QUESTIONS, unresolved topics, or things worth "
        "exploring further based on this content.\n\n"
        "Rules:\n"
        "- Output ONLY a clean numbered list (1. 2. 3. ...), nothing else.\n"
        "- Phrase every item as a question ending with '?'.\n"
        "- For meetings: list unanswered questions or pending topics.\n"
        "- For tutorials/lectures: list questions a learner should investigate next.\n"
        "- ALWAYS produce at least 3 items — never say 'No open questions found'.\n"
        "- Do NOT add intros, headers, markdown, or any text outside the list."
    )
    return chain.invoke(_truncate(transcript))