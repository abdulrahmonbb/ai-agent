from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

print(get_files_info('calculator', '.'))
print(get_files_info('calculator', 'pkg'))
print(get_file_content('calculator', 'main.py'))
print(write_file('calculator', 'main.txt', 'hello'))
