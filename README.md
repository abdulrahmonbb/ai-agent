# AI Agent with Function Calling

This project implements an AI coding agent using Google's Gemini API with function calling capabilities.

## File Structure

### Core Files

- **`call_function.py`**: Contains function schemas and the dispatcher
  - `schema_get_files_info`: Schema for listing directory contents
  - `schema_get_file_content`: Schema for reading file contents
  - `schema_write_file`: Schema for writing content to a file
  - `schema_run_python_file`: Schema for executing Python files
  - `available_functions`: Tool object with all function declarations
  - `call_function()`: Dispatcher that executes functions with injected working_directory

- **`prompts.py`**: System prompt that instructs the LLM on available operations

### Main Scripts

- **`main.py`**: Basic version that prints function calls without executing them
  - Good for testing and understanding how the LLM plans function calls
  
- **`main.py`**: Full agentic version that executes functions and continues conversation
  - Implements the agentic loop
  - Executes function calls
  - Adds results back to conversation
  - Continues until final text response

### Functions

- **`functions/get_files_info.py`**: Lists files in a directory
- **`functions/get_file_content.py`**: Reads file contents
- **`functions/write_file`**: Writes content to files
- **`functions/run_python_file.py`**: Executes Python scripts with optional arguments

## Key Design Decisions

### Security: Working Directory Injection

The `working_directory` parameter is **NOT** exposed to the LLM. Instead:
- The LLM only provides relative paths
- The working directory is injected by `call_function()` 
- This prevents the LLM from accessing files outside the permitted directory

### Function Schemas

Each function has a schema that tells the LLM:
- What the function does (description)
- What parameters it accepts
- Which parameters are required
- The type of each parameter

### Agentic Loop

The full version (`main_agentic.py`) implements an agentic loop:
1. Send user message to LLM
2. If LLM returns function calls:
   - Execute each function
   - Add results to conversation
   - Loop back to step 1
3. If LLM returns text:
   - Print the text
   - Exit loop

## Usage

### Simple Version (just print function calls)

```bash
python main_simple.py "what files are in the root?"
# Output: Calling function: get_files_info({'directory': '.'})

python main_simple.py "what files are in the pkg directory?"
# Output: Calling function: get_files_info({'directory': 'pkg'})
```

### Agentic Version (execute functions)

```bash
python main.py "what files are in the root?"
# Executes get_files_info and returns the actual file list

python main.py "read the main.py file"
# Executes get_file_content and returns the file contents

python main.py "run the tests.py file"
# Executes run_python_file and returns the output

# Specify a different working directory
python main.py "list the files" --working-dir /path/to/dir
```

### Verbose Mode

Add `--verbose` to see token counts and function execution details:

```bash
python main.py "list files and read main.py" --verbose
```

## Example Queries

- "what files are in the root?"
- "what files are in the pkg directory?"
- "read the calculator.py file"
- "run the main.py file"
- "run tests.py"
- "list all Python files and tell me what each one does"
- "run the calculator with the argument '3 + 5'"