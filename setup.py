import sys
from cx_Freeze import setup, Executable


build_exe_options = {"packages": ["os", "datetime"], "excludes": []}

base = None
if sys.platform == "win32":
    base = "Console"  # para execuções em terminal

setup(name="Part2",
      version="0.1",
      description="My GUI application!",
      options={"build_exe": build_exe_options},
      executables=[Executable("Part1.py", base=base)])