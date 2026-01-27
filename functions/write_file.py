import os

def write_file(working_directory, file_path, content):

    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    try:
        common_path = os.path.commonpath([working_dir_abs, target_file_path])
        if common_path != working_dir_abs:
            return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory' 
    
    if os.path.exists(target_file_path):
        # Check if it's a directory
        if os.path.isdir(target_file_path):
           return f"Error: Cannot write to '{file_path}' as it is a directory"
        
    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(target_file_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Write file
    try:
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"