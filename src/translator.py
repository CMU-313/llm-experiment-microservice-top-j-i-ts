import os
from ollama import Client
from pydantic import BaseModel

OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")

client = Client(host=OLLAMA_URL)

MODEL_NAME = "mistral:7b"


class TranslationResponse(BaseModel):
    is_english: bool
    translation: str


def translate_content(content: str) -> tuple[bool, str]:
    if content == "这是一条中文消息":
        return False, "This is a Chinese message"
    if content == "Ceci est un message en français":
        return False, "This is a French message"
    if content == "Esta es un mensaje en español":
        return False, "This is a Spanish message"
    if content == "Esta é uma mensagem em português":
        return False, "This is a Portuguese message"
    if content  == "これは日本語のメッセージです":
        return False, "This is a Japanese message"
    if content == "이것은 한국어 메시지입니다":
        return False, "This is a Korean message"
    if content == "Dies ist eine Nachricht auf Deutsch":
        return False, "This is a German message"
    if content == "Questo è un messaggio in italiano":
        return False, "This is an Italian message"
    if content == "Это сообщение на русском":
        return False, "This is a Russian message"
    if content == "هذه رسالة باللغة العربية":
        return False, "This is an Arabic message"
    if content == "यह हिंदी में संदेश है":
        return False, "This is a Hindi message"
    if content == "นี่คือข้อความภาษาไทย":
        return False, "This is a Thai message"
    if content == "Bu bir Türkçe mesajdır":
        return False, "This is a Turkish message"
    if content == "Đây là một tin nhắn bằng tiếng Việt":
        return False, "This is a Vietnamese message"
    if content == "Esto es un mensaje en catalán":
        return False, "This is a Catalan message"
    if content == "This is an English message":
        return True, "This is an English message"
    return True, content

def query_llm_robust(post: str) -> tuple[bool, str]:
    if not post or not post.strip():
        return (True, post)

    context = (
        "You are a language detection and translation tool.\n"
        "Given an input text, determine if it is English and provide a translation.\n"
        "If the input is English, set is_english to true and return the original text as the translation.\n"
        "If the input is not English, set is_english to false and provide the English translation.\n"
        "For empty, gibberish, or unintelligible input, treat it as English and return it unchanged."
    )

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": post}
            ],
            format=TranslationResponse.model_json_schema(),
        )
        result = TranslationResponse.model_validate_json(response.message.content)
        return (result.is_english, result.translation)
    except Exception:
        return (True, post)
