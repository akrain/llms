import sys

import openai
import os

from openai.types.responses import Response
from openai.types.responses.tool_param import Mcp

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    raise ValueError("OPENAI_API_KEY environment variable not set")

LLM_MODEL = "gpt-4.1-mini-2025-04-14"
EXIT_CMD = "/exit"
CHAT_INSTRUCTIONS = "You are a bot for Gen Alpha kids. You will talk in Gen Alpha lingo"
MCP_INSTRUCTIONS = """You are an assistant for a project's Git repository.
Answer questions about the repository in a concise manner.
Do not add more information than what is asked for.
Do not summarize unless explicitly asked to summarize."""


def chat(instructions: str, message: str, previous_response_id: str | None, stream: bool):
    try:
        response = openai.responses.create(
            model=LLM_MODEL,
            instructions=instructions,
            input=message,
            temperature=1.0,
            previous_response_id=previous_response_id,
            stream=stream,
        )
        return response
    except openai.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API error occurred while processing this request: {e}")


def handle_streaming_events(response: openai.Stream, response_id: str | None):
    print("LLM: ", end="")
    for event in response:
        if event.type == "response.created":
            response_id = event.response.id
        elif event.type == "response.output_text.delta":
            print(event.delta, end="")
        elif event.type == "response.completed":
            print()
        elif event.type == "response.error":
            print("Error event in response", event)
    return response_id


def handle_response(response: Response | openai.Stream, response_id: str | None):
    if isinstance(response, Response):
        print("LLM: " + str(response.output_text))
    else:
        response_id = handle_streaming_events(response, response_id)
    return response_id


def mcp_chat(instructions: str, message: str, previous_response_id: str | None, stream: bool):
    try:
        response = openai.responses.create(
            model=LLM_MODEL,
            instructions=instructions,
            input=message,
            temperature=0.5,
            tools=[Mcp(
                type="mcp", server_label="git-mcp", server_url="https://gitmcp.io/dcos/shakedown",
                require_approval="never", allowed_tools=["fetch_shakedown_documentation"])
            ],
            previous_response_id=previous_response_id,
            stream=stream
        )
        return response
    except openai.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API error occurred while processing this request: {e}")


def main():
    previous_response_id = None
    choice = user_choice()
    chat_func = get_chat_func(choice)
    while True:
        message = input("You: ")
        if message == EXIT_CMD:
            print_exit_msg()
            break
        response = chat_func(CHAT_INSTRUCTIONS, message, previous_response_id, False)
        if response:
            previous_response_id = handle_response(response, previous_response_id)


def print_exit_msg():
    print("Exiting now...")


def get_chat_func(choice):
    chat_func = None
    if choice == "1":
        chat_func = chat
        print("Selected non-MCP chat")
    elif choice == "2":
        chat_func = mcp_chat
        print("Selected MCP chat")
    else:
        print_exit_msg()
        sys.exit(0)
    return chat_func


def user_choice():
    print("\nSelect an option:")
    print("1. Chat")
    print("2. MCP")
    print("Press any other key to Exit")
    choice = input("Enter your choice (1/2): ").strip()
    return choice


if __name__ == "__main__":
    main()
