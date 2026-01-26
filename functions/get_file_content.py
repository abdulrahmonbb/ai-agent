import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    # Construct the absolute target path
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Check if file exists (using target_file_path, not file_path)
    if not os.path.isfile(target_file_path):
        return f"Error: File not found or is not a regular file: '{file_path}'"

    # Security check: ensure target is within working directory
    try:
        common_path = os.path.commonpath([working_dir_abs, target_file_path])
        if common_path != working_dir_abs:
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    except ValueError:
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    
    # Read the file (using target_file_path, not file_path)
    try:
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"
    
    return content