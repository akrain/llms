import sys

from constants import GEMINI_LLM_MODEL, EXIT_CMD, GEMINI_API_KEY, SYSTEM_INSTRUCTIONS
from google import genai
from google.genai import errors, types, chats

try:
    client = genai.Client()
except ValueError:
    raise ValueError(GEMINI_API_KEY, "environment variable not set")

#
# def create_embeddings(inputs: list):
#     try:
#         return openai.embeddings.create(
#             input=inputs,
#             model=EMBEDDINGS_MODEL,
#             dimensions=256,
#         )
#     except openai.APIError as e:
#         # Handle API error here, e.g. retry or log
#         print(f"OpenAI API error occurred while processing this request: {e}")


def chat(gemini_chat: chats.Chat, message: str):
    try:
        response = gemini_chat.send_message_stream(message)
        return response
    except errors.APIError as e:
        print(f"GeminiAI API error occurred while processing this request: {e}")


def handle_response(response):
    if isinstance(response, types.GenerateContentResponse):
        print("LLM: " + response.text)
    else:
        print("LLM: ", end="")
        for chunk in response:
            print(chunk.text);


def main():
    gemini_chat = client.chats.create(
        model=GEMINI_LLM_MODEL,
        config=types.GenerateContentConfig(
            temperature=1.0, system_instruction=SYSTEM_INSTRUCTIONS),
    )
    while True:
        message = input("You: ")
        if message == EXIT_CMD:
            print_exit_msg()
            break
        response = chat(gemini_chat, message)
        if response:
            handle_response(response)


def print_exit_msg():
    print("Exiting now...")


if __name__ == "__main__":
    main()