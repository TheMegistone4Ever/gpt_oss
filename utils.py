from time import time
from typing import Optional, Any, Tuple

from ollama import chat
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam


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
            api_key="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",
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
