import re
from os import getenv
from time import time
from typing import Optional, Any, Tuple, List, Dict

from dotenv import load_dotenv
from ollama import chat
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

load_dotenv()
hf_api_key_1 = getenv("HF_API_KEY_1")
hf_api_key_2 = getenv("HF_API_KEY_2")


def send_chat_request(
        user_message: str,
        sys_message: Optional[str] = None,
        hf: bool = False,
) -> Tuple[Any, float]:
    """
    Send a chat request to a local Ollama instance.

    :param user_message: The message from the user.
    :param sys_message: The system message to set the context.
    :param hf: Whether to use Hugging Face's API instead of a local Ollama instance.
    :return: A tuple containing the response from the model and the elapsed time for the request.
    """

    messages = list()

    if sys_message and len(sys_message.strip()):
        messages.append(ChatCompletionSystemMessageParam(content=sys_message, role="system"))

    if user_message and len(user_message.strip()):
        messages.append(ChatCompletionUserMessageParam(content=user_message, role="user"))

    if hf:
        chat_call = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_api_key_2,
        ).chat.completions.create
    else:
        chat_call = chat

    model_name = (
            ("openai/" if hf else "") +
            "gpt-oss" +
            ("-" if hf else ":") +
            "20b"
    )

    start_time = time()
    response = chat_call(
        model=model_name,
        messages=messages,
    )
    end_time = time()

    return response.choices[0].message.content, end_time - start_time


def parse_harmony_walkthrough(walkthrough: str) -> List[Dict[str, str]]:
    pattern = re.compile(
        r"<\|start\|>(?P<role>\w+)"  # role: user/assistant/system/etc.
        r"(?:<\|channel\|>(?P<channel>\w+))?"  # optional channel
        r"<\|message\|>(?P<content>.*?)"  # message content
        r"<\|end\|>",
        re.DOTALL
    )
    messages = []
    for match in pattern.finditer(walkthrough):
        messages.append({
            "role": match.group("role"),
            "content": match.group("content").strip()
        })

    api_messages = []
    for msg in messages:
        role = msg['role']
        if role in ['developer', 'system']:
            api_messages.append({"role": "system", "content": msg['content']})
        elif role == 'user':
            api_messages.append({"role": "user", "content": msg['content']})
        elif role == 'assistant':
            api_messages.append({"role": "assistant", "content": msg['content']})
        else:
            api_messages.append({"role": None, "content": msg['content']})

    return api_messages
