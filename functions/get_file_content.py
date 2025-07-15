import os
from config import MAX_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        if not (full_path == working_directory or 
                full_path.startswith(working_directory + os.sep)):
            return f"Error: Cannot read file '{file_path}' as it is outside the permitted working directory"
        if not os.path.isfile(full_path):
            return f"Error: File not found or is not a regular file: '{file_path}'"
        with open(full_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
        if len(file_content_string) >= MAX_CHARS:
            return f"{file_content_string} + [...File '{file_path}' truncated at 10000 characters]"
        else:
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory. If not provided, reads from the working directory itself.",                
            )
        }
    )
)
        
