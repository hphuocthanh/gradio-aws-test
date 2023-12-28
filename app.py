import os
from typing import Iterator

import gradio as gr

import requests
import json


MAX_MAX_NEW_TOKENS = 2048
DEFAULT_MAX_NEW_TOKENS = 1024
MAX_INPUT_TOKEN_LENGTH = int(os.getenv("MAX_INPUT_TOKEN_LENGTH", "4096"))

DESCRIPTION = """\
# Llama-2 7B Chat

This Space demonstrates model [Llama-2-7b-chat](https://huggingface.co/meta-llama/Llama-2-7b-chat) by Meta, a Llama 2 model with 7B parameters fine-tuned for chat instructions. Feel free to play with it, or duplicate to run generations without a queue! If you want to run your own service, you can also [deploy the model on Inference Endpoints](https://huggingface.co/inference-endpoints).

🔎 For more details about the Llama 2 family of models and how to use them with `transformers`, take a look [at our blog post](https://huggingface.co/blog/llama2).

🔨 Looking for an even more powerful model? Check out the [13B version](https://huggingface.co/spaces/huggingface-projects/llama-2-13b-chat) or the large [70B model demo](https://huggingface.co/spaces/ysharma/Explore_llamav2_with_TGI).
"""


def generate(
    message: str,
    chat_history: list[tuple[str, str]],
    system_prompt: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.6,
    top_p: float = 0.9,
    top_k: int = 50,
    repetition_penalty: float = 1.2,
) -> Iterator[str]:
    conversation = []
    # if system_prompt:
    #     conversation.append({"role": "system", "content": system_prompt})
    # for user, assistant in chat_history:
    #     conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
    # conversation.append({"role": "user", "content": message})

    API_URL = os.getenv("API_ENVIRONMENT")

    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"data": {"data": "tell me about it"}})
    print(payload)
    response = requests.post(API_URL, data=payload, headers=headers)
    print("response", response.json()["Body"])

    return response.json()["Body"]


def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths


with gr.Blocks() as demo:
    file_output = gr.File()
    upload_button = gr.UploadButton(
        "Click to Upload a File", file_types=["text"], file_count="single", size="lg"
    )
    upload_button.upload(upload_file, upload_button, file_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")
