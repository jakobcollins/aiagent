import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        # Ensure full_path is within the working directory
        if not (full_path == working_directory or
                full_path.startswith(working_directory + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # Creatue the directory if it does not exist
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        # Write the content to the file
        with open(full_path, "w") as file:
            file.write(content)
            with open(full_path, "r") as file_check:
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory. If not provided, writes to the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided, an empty file will be created.",
            )
        }
    )
)