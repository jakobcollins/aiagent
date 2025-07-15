import os
from google import genai
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    func_dict = {"get_files_info": get_files_info(working_directory="./calculator"),
                "get_file_content": get_file_content(working_directory="./calculator"),
                "run_python_file": run_python_file(working_directory="./calculator"),
                "write_file": write_file(working_directory="./calculator")}