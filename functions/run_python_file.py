import os
import subprocess


def run_python_file(working_directory, file_path, args=None):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        try:
            common_path = os.path.commonpath([working_dir_abs, target_file_path])
            if common_path != working_dir_abs:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if target_file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_dir_abs, timeout=30, capture_output=True, text=True
        )

        output_strings = []

        if result.returncode != 0:
            output_strings.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_strings.append("No output produces")
        else:
            if result.stdout:
                output_strings.append(f"STDOUT:\n{result.stdout}")

            if result.stderr:
                output_strings.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_strings)
    except Exception as e:
        return f"Error: executing python file {e}"
