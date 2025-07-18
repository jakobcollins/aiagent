import os
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    func = function_map.get(function_call_part.name)
    if not func:
        return types.Content(
            role="model",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                     response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    some_args = function_call_part.args.copy()
    if "working_directory" not in some_args:
        some_args["working_directory"] = "./calculator"
    function_result = func(**some_args)
    return types.Content(
        role="model",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
             )
         ],
    )