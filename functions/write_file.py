import os

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