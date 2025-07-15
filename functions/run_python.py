import os 
import subprocess

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        if not (full_path == working_directory or
                full_path.startswith(working_directory + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error: {str(e)}"
    # Execute the Python file
    result = subprocess.run(['python3', full_path], timeout=30, capture_output=True, text=True)
    output_lines = []
    try:
        if result.stdout.strip():
            output_lines.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr.strip():
            output_lines.append(f"STDERR: {result.stderr.strip()}")
        if not output_lines:
            output_lines.append("No output produced.")
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}.")
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"