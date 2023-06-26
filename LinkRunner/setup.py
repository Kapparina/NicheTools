from cx_Freeze import setup, Executable
from pathlib import Path


# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': ["rapidfuzz"],
    'excludes': ["colorama",
                 "curses",
                 "openpyxl",
                 "sqlalchemy",
                 "sqlite3"]}

base = 'console'

executables = [
    Executable(Path('./LinkRunner/lr_main.py'), base=base, target_name ='LinkRunner')
]

setup(name='LinkRunner',
      version = '1.0.0',
      description = 'Allows for filtering, searching and following hyperlinks.',
      options = {'build_exe': build_options},
      executables = executables)
