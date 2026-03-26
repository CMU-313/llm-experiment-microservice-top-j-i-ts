from src.translator import translate_content, query_llm_robust, client
from mock import patch


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass

@patch.object(client, 'chat')
def test_unexpected_language(mocker):
    mocker.return_value.message.content = "I don't understand your request"
    result = query_llm_robust("Hier ist dein erstes Beispiel.")
    assert result == (True, "Hier ist dein erstes Beispiel.")

@patch.object(client, 'chat')
def test_empty_response(mocker):
    mocker.return_value.message.content = ""
    result = query_llm_robust("Hello world")
    assert result == (True, "Hello world")

@patch.object(client, 'chat')
def test_exception_from_ollama(mocker):
    mocker.side_effect = Exception("Connection refused")
    result = query_llm_robust("Bonjour tout le monde")
    assert result == (True, "Bonjour tout le monde")

@patch.object(client, 'chat')
def test_partial_format_missing_translation(mocker):
    mocker.return_value.message.content = "IS_ENGLISH: False"
    result = query_llm_robust("Hola amigos")
    assert result == (True, "Hola amigos")

@patch.object(client, 'chat')
def test_normal_english_input(mocker):
    mocker.return_value.message.content = "IS_ENGLISH: True\nTRANSLATION: Hello friend"
    result = query_llm_robust("Hello friend")
    assert result == (True, "Hello friend")

@patch.object(client, 'chat')
def test_normal_non_english_input(mocker):
    mocker.return_value.message.content = "IS_ENGLISH: False\nTRANSLATION: Hello friend"
    result = query_llm_robust("Hola amigo")
    assert result == (False, "Hello friend")