import os

def get_files_info(working_directory, directory="."):

    if not directory:
        return f'Error: "{directory}" is not a directory'
    
    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(absolute_path, directory))

    if not os.path.isdir(target_directory):
        return f"Error: Directory {target_directory} does not exist"

    valid_target_dir = os.path.commonpath([absolute_path, target_directory]) == absolute_path

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    items_info = []

    try:    
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            try:
                file_size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                item_info = f"- {item}: file_size={file_size}, is_dir={is_dir}"
                items_info.append(item_info)
            except Exception as e:
                item_info = f"- {item}: ERROR accessing file"
                items_info.append(item_info)
    except Exception as e:
        return f"Error accessing directory: {e}"
    
    content = "\n".join(items_info)
    return content