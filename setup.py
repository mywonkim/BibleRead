import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']
base = None

if sys.platform == "win32":
      base = "Win32GUI"

setup(name='BibleRead',
      version='1.0',
      description='Bible Reading',
      options={'build_exe' : {'include_files' : include_files}},
      executables = [Executable('main.py')])
