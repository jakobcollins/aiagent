import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT, MODEL
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from aiagent!")


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    if len(sys.argv) < 2:
        print("Usage: python main.py '<your prompt>'")
        sys.exit(1)
    elif len(sys.argv) >= 2:
        user_prompt = sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        response = client.models.generate_content(
                model=MODEL, 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=SYSTEM_PROMPT),
            )
        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            print("User prompt:", user_prompt)
            if response.function_calls:
                for function_call_part in response.function_calls:
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            if response.text == None:
                print("No response text generated.")
            else:
                print(response.text)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        else:
            if response.function_calls:
                for function_call_part in response.function_calls:
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            if response.text == None:
                print("No response text generated.")
            else:
                print(response.text)


if __name__ == "__main__":
    main()
