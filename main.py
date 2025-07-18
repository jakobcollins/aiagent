import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT, MODEL
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

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
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py '<your prompt>'")
            sys.exit(1)
        else:
            user_prompt = sys.argv[1]
            messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]
            calls = 0
            while calls < 20:
                calls += 1
                response = client.models.generate_content(
                        model = MODEL, 
                        contents = messages,
                        config = types.GenerateContentConfig(
                            tools = [available_functions], system_instruction = SYSTEM_PROMPT),
                    )
                for candidate in response.candidates:
                    messages.append(candidate.content)
                verbose_mode = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
                if response.function_calls:
                    for function_call_part in response.function_calls:
                        function_call_result = call_function(function_call_part, verbose= verbose_mode)
                        # Check for result attribute and print as required
                        parts = function_call_result.parts
                        if not parts or not hasattr(parts[0], "function_response") or not hasattr(parts[0].function_response, "response"):
                            raise Exception("Function call did not return a valid result!")
                        # Convert function response to a tool message and append it to messages
                        tool_message = types.Content(
                            role = "model",
                            parts = [types.Part(text=json.dumps(parts[0].function_response.response, indent=2))]
                        )
                        messages.append(tool_message)
                        if verbose_mode:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                done = False
                for candidate in response.candidates:
                    has_text = any(p.text for p in candidate.content.parts)
                    has_function_call = any(p.function_call for p in candidate.content.parts)
                    if has_text and not has_function_call:
                        done = True
                if done:
                    break 
            if response.text is None:
                print("No response text received.")
                return
            else:               
                print(response.text)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
