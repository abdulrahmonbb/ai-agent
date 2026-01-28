from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file

# Function schemas for Gemini API
# Note: working_directory is NOT exposed to the LLM - it's injected by our code for security

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file relative to the working directory. Returns the file content or an error message.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file relative to the working directory. Returns the output (stdout/stderr) or an error message.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)

# Available functions tool for Gemini API
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
    ],
)


def call_function(function_name, args, working_directory="calculator"):
    """
    Execute a function by name with the provided arguments.
    The working_directory is injected here for security - the LLM doesn't control it.
    
    Args:
        function_name: Name of the function to call
        args: Dictionary of arguments from the LLM
        working_directory: The permitted working directory (injected, not from LLM)
    
    Returns:
        The result of the function call as a string
    """
    if function_name == "get_file_content":
        return get_file_content(
            working_directory=working_directory,
            file_path=args.get("file_path")
        )
    
    elif function_name == "get_files_info":
        # The LLM calls it "directory" but our function expects "path"
        return get_files_info(
            working_directory=working_directory,
            path=args.get("directory", ".")
        )
    
    elif function_name == "run_python_file":
        return run_python_file(
            working_directory=working_directory,
            file_path=args.get("file_path"),
            args=args.get("args")
        )
    
    else:
        return f"Error: Unknown function '{function_name}'"