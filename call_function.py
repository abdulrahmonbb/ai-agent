from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Function schemas for Gemini API
# Note: working_directory is NOT exposed to the LLM - it's injected by our code for security

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status. If no directory is specified, lists the working directory itself.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory. Defaults to '.' (the working directory itself) if not specified.",
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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file to be written to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to be written to file"
            ),
        },
        required=["file_path", "content"],
    )
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
        schema_write_file,
        schema_run_python_file,
    ],
)

# Map of function names to actual functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call, verbose=False):
    """
    Execute a function call and return the result.
    The working_directory is injected here for security - the LLM doesn't control it.
    
    Args:
        function_call: A types.FunctionCall object with name and args properties
        verbose: If True, print detailed function call information
    
    Returns:
        A types.Content object with the function result
    """
    # Get function name (ensure it's a string)
    function_name = function_call.name or ""
    
    # Print function call info
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Make a shallow copy of args and inject working_directory
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    
    # Handle parameter name mapping for get_files_info
    if function_name == "get_files_info":
        # Ensure directory parameter exists, default to "." if not provided
        if "directory" not in args:
            args["directory"] = "."
    
    # Call the function with unpacked arguments
    function_result = function_map[function_name](**args)
    
    # Return the result as a types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )