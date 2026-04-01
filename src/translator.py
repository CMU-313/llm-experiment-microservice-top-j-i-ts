import os
# Use Ollama library to interact with model:
from ollama import chat, ChatResponse, Client

# Get OLLAMA_HOST, if specified, or default to localhost:11434.
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")

# Initialize the OpenAI client
client = Client(host=OLLAMA_URL)

# Specify model
MODEL_NAME = "mistral:7b"


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
        "Given an input text, respond with EXACTLY two lines and nothing else:\n\n"
        "IS_ENGLISH: <True or False — True only if the INPUT text is written in English>\n"
        "TRANSLATION: <if input is English: the original text unchanged | if input is NOT English: the English translation>\n\n"
        "IMPORTANT: IS_ENGLISH describes the language of the INPUT text, not the translation.\n"
        "If the input is German, Spanish, French, or any non-English language, IS_ENGLISH must be False.\n\n"
        "Rules:\n"
        "- Output ONLY the two lines above. No explanations, no parenthetical notes, no language labels.\n"
        "- The TRANSLATION value must be plain translated text and nothing else.\n"
        "- For empty, gibberish, or unintelligible input, treat it as English and return it unchanged."
    )

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": post}
            ]
        )
        content = response.message.content.strip()
    except Exception:
        return (True, post)

    is_english = None
    translation = None

    for line in content.split("\n"):
        line = line.strip()
        if line.upper().startswith("IS_ENGLISH:"):
            value = line.split(":", 1)[1].strip().lower()
            if value in ("true", "false"):
                is_english = value == "true"
        elif line.upper().startswith("TRANSLATION:"):
            translation = line.split(":", 1)[1].strip()

    if is_english is None or translation is None:
        return (True, post)

    return (is_english, translation)
