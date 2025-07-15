import os

def get_files_info(working_directory, directory=None):
    # Get absolute paths
    working_directory = os.path.abspath(working_directory)
    if directory:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
    else:
        full_path = working_directory
    # Ensure full_path is within the working directory
    if not (full_path == working_directory or 
    full_path.startswith(working_directory + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    # Build the file information
    info_list = []
    try:
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            info_list.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(info_list)
    except Exception as e:
        return f"Error: {str(e)}"   
